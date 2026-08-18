from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime
import uvicorn

from data.fetcher import fetch_price_data
from data.rs_calculator import calculate_relative_strength
from data.tickers import TICKERS

app = FastAPI(title="Market Relative Strength")
templates = Jinja2Templates(directory="templates")

# Globaler Cache
_cache = {
    "data": None,
    "timestamp": None
}


def load_data():
    """Lädt die Daten und speichert sie im Cache."""
    print("Lade frische Daten von Tiingo...")
    closes = fetch_price_data(period="1mo")
    rs_data = calculate_relative_strength(closes)
    _cache["data"] = rs_data
    _cache["timestamp"] = datetime.now()
    print(f"✅ {len(rs_data)} Einträge geladen")
    return rs_data


@app.on_event("startup")
async def startup_event():
    """Beim App-Start einmal Daten laden."""
    try:
        load_data()
    except Exception as e:
        print(f"Fehler beim initialen Laden: {e}")
        _cache["data"] = []


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, group: str = "all"):
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
            "last_update": _cache["timestamp"].strftime("%Y-%m-%d %H:%M") if _cache["timestamp"] else "-"
        }
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)