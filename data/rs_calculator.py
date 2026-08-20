import pandas as pd
import numpy as np
from .tickers import TICKERS, BENCHMARK


def _return(series: pd.Series, days: int) -> float | None:
    """Performance über ca. N Handelstage."""
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
    """Relative Performance vs SPY über N Handelstage."""
    aligned = pd.concat([ticker_s, spy_s], axis=1, join="inner").dropna()
    if aligned.shape[1] < 2 or len(aligned) < days + 1:
        return None
    t = aligned.iloc[:, 0]
    b = aligned.iloc[:, 1]
    t_ret = t.iloc[-1] / t.iloc[-(days + 1)] - 1
    b_ret = b.iloc[-1] / b.iloc[-(days + 1)] - 1
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
    """Perzentil 0–100 innerhalb des Universums."""
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


def calculate_relative_strength(closes: pd.DataFrame) -> list[dict]:
    if BENCHMARK not in closes.columns:
        raise ValueError("SPY Benchmark fehlt in den Daten")

    # Index ggf. timezone-naiv machen
    if getattr(closes.index, "tz", None) is not None:
        closes = closes.copy()
        closes.index = closes.index.tz_localize(None)

    spy = closes[BENCHMARK].dropna()

    rel_1d_map: dict[str, float | None] = {}
    rel_1w_map: dict[str, float | None] = {}
    rel_1m_map: dict[str, float | None] = {}
    rel_ytd_map: dict[str, float | None] = {}

    results: list[dict] = []

    for group_name, group_tickers in TICKERS.items():
        for ticker, name in group_tickers.items():
            if ticker not in closes.columns:
                continue

            s = closes[ticker].dropna()
            if len(s) < 5:
                continue

            # Absolute Returns
            abs_1d = _return(s, 1)
            abs_1w = _return(s, 5)
            abs_1m = _return(s, 21)
            abs_ytd = _ytd_return(s)

            # Relative Returns vs SPY
            r1d = _rel_return(s, spy, 1)
            r1w = _rel_return(s, spy, 5)
            r1m = _rel_return(s, spy, 21)
            rytd = _rel_ytd(s, spy)

            rel_1d_map[ticker] = r1d
            rel_1w_map[ticker] = r1w
            rel_1m_map[ticker] = r1m
            rel_ytd_map[ticker] = rytd

            # RS-Ratio (ca. 3 Monate, rebased auf 100)
            aligned = pd.concat([s, spy], axis=1, join="inner").dropna()
            if len(aligned) < 10:
                continue

            t = aligned.iloc[:, 0]
            b = aligned.iloc[:, 1]
            window = min(63, len(t))
            ratio = (t.iloc[-window:] / b.iloc[-window:]) * 100
            ratio = ratio / ratio.iloc[0] * 100
            rs_last = float(ratio.iloc[-1])

            # Sparkline (letzte 22 Punkte, 0–100)
            spark = ratio.tail(22).values
            if len(spark) > 1 and spark.max() > spark.min():
                spark_norm = ((spark - spark.min()) / (spark.max() - spark.min()) * 100).tolist()
            else:
                spark_norm = [50.0] * max(len(spark), 1)

            results.append(
                {
                    "group": group_name,
                    "ticker": ticker,
                    "name": name,
                    "last_price": _round(float(s.iloc[-1])),
                    "abs_1d": _round(abs_1d),
                    "abs_1w": _round(abs_1w),
                    "abs_1m": _round(abs_1m),
                    "abs_ytd": _round(abs_ytd),
                    "rel_1d": _round(r1d),
                    "rel_1w": _round(r1w),
                    "rel_1m": _round(r1m),
                    "rel_ytd": _round(rytd),
                    "rs_last": _round(rs_last),
                    "sparkline": spark_norm,
                    # Perzentile werden nach dem Loop gesetzt
                    "pct_rel_1d": None,
                    "pct_rel_1w": None,
                    "pct_rel_1m": None,
                    "pct_rel_ytd": None,
                    "pct_1m_ago": None,
                    "pct_3m_ago": None,
                    "pct_6m_ago": None,
                }
            )

    # Perzentile auf Basis der Relative Returns
    for row in results:
        t = row["ticker"]
        row["pct_rel_1d"] = _round(_percentile(rel_1d_map, t), 0)
        row["pct_rel_1w"] = _round(_percentile(rel_1w_map, t), 0)
        row["pct_rel_1m"] = _round(_percentile(rel_1m_map, t), 0)
        row["pct_rel_ytd"] = _round(_percentile(rel_ytd_map, t), 0)

    # Default-Sort: 1M Relative Performance absteigend
    results = sorted(
        results,
        key=lambda x: x["rel_1m"] if x["rel_1m"] is not None else -9999,
        reverse=True,
    )
    return results