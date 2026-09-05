import pandas as pd
import numpy as np
from .tickers import TICKERS, BENCHMARK

PERIODS = {
    "1w": 5,
    "1m": 21,
    "3m": 63,
    "1y": 252,
}

# 6M Handelslage für das 1M-RS-Balkensparkline (~126 Handelstage)
RS_BAR_LOOKBACK = 21
RS_BAR_HISTORY = 126
RS_BAR_WIDTH = 140
RS_BAR_HEIGHT = 28


def _return(series: pd.Series, days: int) -> float | None:
    s = series.dropna()
    if len(s) < days + 1:
        return None
    return float((s.iloc[-1] / s.iloc[-(days + 1)] - 1) * 100)


def _ytd_return(series: pd.Series) -> float | None:
    s = series.dropna()
    if s.empty:
        return None
    year = s.index[-1].year
    ytd = s[s.index.year == year]
    if len(ytd) < 2:
        return None
    return float((ytd.iloc[-1] / ytd.iloc[0] - 1) * 100)


def _rel_return(ticker_s: pd.Series, spy_s: pd.Series, days: int) -> float | None:
    aligned = pd.concat([ticker_s, spy_s], axis=1, join="inner").dropna()
    if aligned.shape[1] < 2 or len(aligned) < days + 1:
        return None
    t = aligned.iloc[:, 0]
    b = aligned.iloc[:, 1]
    t_ret = t.iloc[-1] / t.iloc[-(days + 1)] - 1
    b_ret = b.iloc[-1] / b.iloc[-(days + 1)] - 1
    return float((t_ret - b_ret) * 100)


def _rel_return_offset(ticker_s: pd.Series, spy_s: pd.Series, days: int, offset: int = 0) -> float | None:
    aligned = pd.concat([ticker_s, spy_s], axis=1, join="inner").dropna()
    if aligned.shape[1] < 2 or len(aligned) < days + 1 + offset:
        return None
    t = aligned.iloc[:, 0]
    b = aligned.iloc[:, 1]
    end = -1 - offset
    start = end - days
    t_ret = t.iloc[end] / t.iloc[start] - 1
    b_ret = b.iloc[end] / b.iloc[start] - 1
    return float((t_ret - b_ret) * 100)


def _rel_ytd(ticker_s: pd.Series, spy_s: pd.Series) -> float | None:
    aligned = pd.concat([ticker_s, spy_s], axis=1, join="inner").dropna()
    if aligned.empty or aligned.shape[1] < 2:
        return None
    year = aligned.index[-1].year
    a = aligned[aligned.index.year == year]
    if len(a) < 2:
        return None
    t = a.iloc[:, 0]
    b = a.iloc[:, 1]
    return float((t.iloc[-1] / t.iloc[0] - b.iloc[-1] / b.iloc[0]) * 100)


def _percentile(values: dict[str, float | None], ticker: str) -> float | None:
    valid = {
        k: v
        for k, v in values.items()
        if v is not None and not (isinstance(v, float) and np.isnan(v))
    }
    if ticker not in valid or len(valid) < 2:
        return None
    arr = np.array(list(valid.values()), dtype=float)
    return float((arr < valid[ticker]).sum() / len(arr) * 100)


def _round(v: float | None, digits: int = 2) -> float | None:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return None
    return round(float(v), digits)


def _rolling_rs_ratio(ticker_s: pd.Series, spy_s: pd.Series, lookback: int = 21) -> pd.Series:
    """
    Tägliche 1M-Relativstärke als Ratio:
        RS = (P_t / P_{t-21}) / (SPY_t / SPY_{t-21})
    Werte >= 1.0 bedeuten Outperformance vs. SPY über 1 Monat.
    """
    aligned = pd.concat([ticker_s, spy_s], axis=1, join="inner").dropna()
    if aligned.shape[1] < 2 or len(aligned) < lookback + 2:
        return pd.Series(dtype=float)

    t = aligned.iloc[:, 0]
    b = aligned.iloc[:, 1]
    t_ret = t / t.shift(lookback)
    b_ret = b / b.shift(lookback)
    ratio = t_ret / b_ret
    return ratio.replace([np.inf, -np.inf], np.nan).dropna()


def _rs_bar_sparkline(
    ticker_s: pd.Series,
    spy_s: pd.Series,
    lookback: int = RS_BAR_LOOKBACK,
    history: int = RS_BAR_HISTORY,
    width: int = RS_BAR_WIDTH,
    height: int = RS_BAR_HEIGHT,
) -> list[dict]:
    """Balken-Koordinaten für ein 6M-Sparkline der rollierenden 1M-RS-Ratio."""
    series = _rolling_rs_ratio(ticker_s, spy_s, lookback=lookback)
    if series.empty:
        return []

    values = series.iloc[-history:].astype(float).tolist()
    if len(values) < 2:
        return []

    mid = height / 2.0
    dev = max(abs(v - 1.0) for v in values)
    dev = max(dev, 0.02)

    n = len(values)
    bar_w = width / n
    gap = max(bar_w * 0.18, 0.15)
    draw_w = max(bar_w - gap, 0.35)

    bars: list[dict] = []
    for i, v in enumerate(values):
        above = v >= 1.0
        mag = min(abs(v - 1.0) / dev, 1.0) * (mid - 1.0)
        mag = max(mag, 0.5)
        if above:
            y = mid - mag
            h = mag
        else:
            y = mid
            h = mag
        bars.append(
            {
                "x": round(i * bar_w, 3),
                "y": round(y, 3),
                "w": round(draw_w, 3),
                "h": round(h, 3),
                "up": above,
                "v": round(v, 4),
            }
        )
    return bars


def calculate_relative_strength(closes: pd.DataFrame) -> list[dict]:
    if BENCHMARK not in closes.columns:
        raise ValueError("SPY Benchmark fehlt in den Daten")

    if getattr(closes.index, "tz", None) is not None:
        closes = closes.copy()
        closes.index = closes.index.tz_localize(None)

    spy = closes[BENCHMARK].dropna()
    rel_maps = {p: {} for p in list(PERIODS.keys()) + ["ytd"]}
    results: list[dict] = []

    for group_name, group_tickers in TICKERS.items():
        for ticker, name in group_tickers.items():
            if ticker not in closes.columns:
                continue

            s = closes[ticker].dropna()
            if len(s) < 5:
                continue

            row = {
                "group": group_name,
                "ticker": ticker,
                "name": name,
                "last_price": _round(float(s.iloc[-1])),
            }

            for key, days in PERIODS.items():
                row[f"abs_{key}"] = _round(_return(s, days))
            row["abs_ytd"] = _round(_ytd_return(s))

            for key, days in PERIODS.items():
                r = _rel_return(s, spy, days)
                row[f"rel_{key}"] = _round(r)
                rel_maps[key][ticker] = r

            rytd = _rel_ytd(s, spy)
            row["rel_ytd"] = _round(rytd)
            rel_maps["ytd"][ticker] = rytd

            rel_now = _rel_return_offset(s, spy, PERIODS["1m"], 0)
            rel_prev = _rel_return_offset(s, spy, PERIODS["1m"], 21)
            if rel_now is None or rel_prev is None:
                row["rel_1m_chg"] = None
            else:
                row["rel_1m_chg"] = _round(rel_now - rel_prev)

            aligned = pd.concat([s, spy], axis=1, join="inner").dropna()
            spark_norm = []
            if len(aligned) >= 5:
                t = aligned.iloc[:, 0]
                b = aligned.iloc[:, 1]
                window = min(21, len(t))
                if window >= 2:
                    ratio = t.iloc[-window:] / b.iloc[-window:]
                    ratio = ratio / ratio.iloc[0] * 100.0
                    spark = ratio.values.astype(float)
                    lo, hi = float(spark.min()), float(spark.max())
                    if hi > lo:
                        spark_norm = ((spark - lo) / (hi - lo) * 100.0).tolist()
                    else:
                        spark_norm = [50.0] * len(spark)

            row["sparkline"] = spark_norm
            row["rs_bars"] = _rs_bar_sparkline(s, spy)
            row["rs_bar_width"] = RS_BAR_WIDTH
            row["rs_bar_height"] = RS_BAR_HEIGHT
            results.append(row)

    for row in results:
        t = row["ticker"]
        for key in list(PERIODS.keys()) + ["ytd"]:
            row[f"pct_{key}"] = _round(_percentile(rel_maps[key], t), 0)

    results = sorted(
        results,
        key=lambda x: x["rel_1m"] if x.get("rel_1m") is not None else -9999,
        reverse=True,
    )
    return results