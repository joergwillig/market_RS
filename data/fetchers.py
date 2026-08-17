import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from .tickers import ALL_TICKERS, BENCHMARK

def fetch_price_data(period: str = "3mo") -> pd.DataFrame:
    """
    Lädt Daily Close für alle Ticker + SPY.
    Gibt ein DataFrame mit MultiIndex (Ticker, Date) zurück.
    """
    data = yf.download(
        ALL_TICKERS,
        period=period,
        interval="1d",
        group_by="ticker",
        auto_adjust=True,
        threads=True,
        progress=False
    )

    # Nur Close-Preise extrahieren
    if len(ALL_TICKERS) == 1:
        closes = data[["Close"]].rename(columns={"Close": ALL_TICKERS[0]})
    else:
        closes = data.xs("Close", axis=1, level=1)

    closes = closes.dropna(how="all")
    return closes