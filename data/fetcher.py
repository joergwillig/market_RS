import os
import time
import requests
import pandas as pd
from datetime import datetime, timedelta
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


def fetch_single_ticker(
    ticker: str,
    start_date: str | None = None,
) -> pd.Series | None:
    """
    Holt Daily Adjusted Close von Tiingo.
    Standard: ca. 15 Monate Historie (YTD + 6M Perzentile).
    """
    if start_date is None:
        start_date = (datetime.utcnow() - timedelta(days=450)).strftime("%Y-%m-%d")

    api_key = get_api_key()

    url = f"{BASE_URL}/{ticker}/prices"
    params = {
        "startDate": start_date,
        "token": api_key,
    }
    headers = {
        "Content-Type": "application/json",
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

        # Zeitzone entfernen, falls vorhanden (einheitlicher Index)
        if getattr(df.index, "tz", None) is not None:
            df.index = df.index.tz_localize(None)

        if "adjClose" in df.columns:
            s = df["adjClose"]
        else:
            s = df["close"]

        s.name = ticker
        return s

    except Exception as e:
        print(f"  ❌ {ticker}: {e}")
        return None


def fetch_price_data(period: str = "1y", delay: float = 0.3) -> pd.DataFrame:
    """
    Lädt alle Ticker einzeln über Tiingo.

    period:
      - wird hier vor allem für die Anzeige/Logs genutzt
      - wir behalten bewusst genug Historie für YTD und 6M-Berechnungen
    """
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

    # Einheitliche Zeitzone / naive Timestamps
    if getattr(closes.index, "tz", None) is not None:
        closes.index = closes.index.tz_localize(None)

    print(f"\n✅ Erfolgreich: {len(closes.columns)} von {len(ALL_TICKERS)} Tickern")
    print(f"   Zeitraum: {closes.index.min().date()} → {closes.index.max().date()}")

    return closes