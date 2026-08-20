import os
import secrets
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import uvicorn

from data.fetcher import fetch_price_data
from data.rs_calculator import calculate_relative_strength
from data.tickers import TICKERS

app = FastAPI(title="Market Relative Strength")
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()

_cache = {
    "data": None,
    "timestamp": None,
}

TZ = ZoneInfo("Europe/Berlin")


def verify_password(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = os.getenv("APP_USERNAME", "admin")
    correct_password = os.getenv("APP_PASSWORD")

    # Wenn kein Passwort gesetzt ist: kein Schutz (nur Dev)
    if not correct_password:
        return credentials.username

    user_ok = secrets.compare_digest(credentials.username, correct_username)
    pass_ok = secrets.compare_digest(credentials.password, correct_password)

    if not (user_ok and pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ungültige Anmeldedaten",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def load_data():
    print(f"[{datetime.now(TZ)}] Lade frische Daten von Tiingo...")
    closes = fetch_price_data(period="1mo")
    rs_data = calculate_relative_strength(closes)
    _cache["data"] = rs_data
    _cache["timestamp"] = datetime.now(TZ)
    print(f"[{datetime.now(TZ)}] ✅ {len(rs_data)} Einträge geladen")
    return rs_data


scheduler = BackgroundScheduler(timezone=TZ)
scheduler.add_job(
    load_data,
    trigger=CronTrigger(hour=6, minute=0, timezone=TZ),
    id="daily_refresh",
    replace_existing=True,
)


@app.on_event("startup")
async def startup_event():
    try:
        load_data()
    except Exception as e:
        print(f"Fehler beim initialen Laden: {e}")
        _cache["data"] = []

    if not scheduler.running:
        scheduler.start()
        print("Scheduler gestartet – tägliches Update um 06:00 Europe/Berlin")


@app.on_event("shutdown")
async def shutdown_event():
    if scheduler.running:
        scheduler.shutdown(wait=False)


@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    group: str = "all",
    sort: str = "rel_1m",
    dir: str = "desc",
    username: str = Depends(verify_password),
):
    data = list(_cache["data"] or [])

    if group != "all":
        data = [d for d in data if d["group"] == group]

    reverse = dir != "asc"

    def key_fn(x):
        v = x.get(sort)
        if v is None:
            return -9999 if reverse else 9999
        return v

    try:
        data = sorted(data, key=key_fn, reverse=reverse)
    except Exception:
        pass

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "data": data,
            "groups": list(TICKERS.keys()),
            "active_group": group,
            "sort": sort,
            "dir": dir,
            "last_update": _cache["timestamp"].strftime("%Y-%m-%d %H:%M")
            if _cache["timestamp"]
            else "-",
        },
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)