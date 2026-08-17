from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from datetime import datetime

from data.fetcher import fetch_price_data
from data.rs_calculator import calculate_relative_strength
from data.tickers import TICKERS

app = FastAPI(title="Market Relative Strength")
templates = Jinja2Templates(directory="templates")

# Einfacher In-Memory Cache (für den Start)
_cache = {"data": None, "timestamp": None}

def get_rs_data():
    now = datetime.now()
    # Cache 30 Minuten
    if _cache["data"] is None or (now - _cache["timestamp"]).seconds > 1800:
        print("Lade frische Daten von yfinance...")
        closes = fetch_price_data(period="3mo")
        rs_data = calculate_relative_strength(closes)
        _cache["data"] = rs_data
        _cache["timestamp"] = now
    return _cache["data"]

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, group: str = "all"):
    data = get_rs_data()

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
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)