import os
import secrets
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime
import uvicorn

from data.fetcher import fetch_price_data
from data.rs_calculator import calculate_relative_strength
from data.tickers import TICKERS

app = FastAPI(title="Market Relative Strength")
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()

_cache = {
    "data": None,
    "timestamp": None
}


def verify_password(credentials: HTTPBasicCredentials = Depends(security)):
    """Prüft Benutzername + Passwort."""
    correct_username = os.getenv("APP_USERNAME", "admin")
    correct_password = os.getenv("APP_PASSWORD")

    if not correct_password:
        # Kein Passwort gesetzt → kein Schutz (nur für lokalen Test)
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
    print("Lade frische Daten von Tiingo...")
    closes = fetch_price_data(period="1mo")
    rs_data = calculate_relative_strength(closes)
    _cache["data"] = rs_data
    _cache["timestamp"] = datetime.now()
    print(f"✅ {len(rs_data)} Einträge geladen")
    return rs_data


@app.on_event("startup")
async def startup_event():
    try:
        load_data()
    except Exception as e:
        print(f"Fehler beim initialen Laden: {e}")
        _cache["data"] = []


@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    group: str = "all",
    username: str = Depends(verify_password),
):
    data = _cache["data"] or []

    if group != "all":
        data = [d for d in data if d["group"] == group]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "data": data,
            "groups": list(TICKERS.keys()),
            "active_group": group,
            "last_update": _cache["timestamp"].strftime("%Y-%m-%d %H:%M") if _cache["timestamp"] else "-",
        },
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)