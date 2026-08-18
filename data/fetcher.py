import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from .tickers import ALL_TICKERS, BENCHMARK

load_dotenv()

BASE_URL = "https://api.tiingo.com/tiingo/daily"


def get_api_key() -> str:
    key = os.getenv("TIINGO_API_KEY")
    if not key:
        raise ValueError(
            f"TIINGO_API_KEY fehlt. "
            f"Env-Keys mit TIINGO/API: {[k for k in os.environ.keys() if 'TIINGO' in k.upper() or 'API' in k.upper()]}"
        )
    return key


def fetch_single_ticker(ticker: str, start_date: str = "2025-01-01") -> pd.Series | None:
    """Holt Daily Adjusted Close von Tiingo."""
    api_key = get_api_key()

    url = f"{BASE_URL}/{ticker}/prices"
    params = {
        "startDate": start_date,
        "token": api_key,
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        r = requests.get(url, params=params, headers=headers, timeout=30)

        if r.status_code != 200:
            print(f"  ⚠️  {ticker}: HTTP {r.status_code} – {r.text[:120]}")
            return None

        data = r.json()

        if not data:
            print(f"  ⚠️  {ticker}: keine Daten")
            return None

        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date").sort_index()

        if "adjClose" in df.columns:
            s = df["adjClose"]
        else:
            s = df["close"]

        s.name = ticker
        return s

    except Exception as e:
        print(f"  ❌ {ticker}: {e}")
        return None


def fetch_price_data(period: str = "3mo", delay: float = 0.3) -> pd.DataFrame:
    """Lädt alle Ticker einzeln über Tiingo."""
    print(f"Lade {len(ALL_TICKERS)} Ticker über Tiingo...\n")

    series_list = []

    for i, ticker in enumerate(ALL_TICKERS, 1):
        print(f"[{i}/{len(ALL_TICKERS)}] {ticker} ...", end=" ")
        s = fetch_single_ticker(ticker)

        if s is not None and not s.empty:
            series_list.append(s)
            print(f"OK ({len(s)} Tage)")
        else:
            print("FEHLGESCHLAGEN")

        if i < len(ALL_TICKERS):
            time.sleep(delay)

    if not series_list:
        raise ValueError("Keine Ticker konnten geladen werden!")

    closes = pd.concat(series_list, axis=1).sort_index()

    # Letzte ~30 Tage (ohne deprecated .last())
    if period == "1mo":
        cutoff = closes.index.max() - pd.Timedelta(days=35)
        closes = closes.loc[closes.index >= cutoff]
    elif period == "3mo":
        cutoff = closes.index.max() - pd.Timedelta(days=95)
        closes = closes.loc[closes.index >= cutoff]

    print(f"\n✅ Erfolgreich: {len(closes.columns)} von {len(ALL_TICKERS)} Tickern")
    print(f"   Zeitraum: {closes.index.min().date()} → {closes.index.max().date()}")

    return closes