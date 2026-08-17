import pandas as pd
import numpy as np
from .tickers import TICKERS, BENCHMARK

def calculate_relative_strength(closes: pd.DataFrame, lookback: int = 22) -> dict:
    """
    Berechnet 1-Month Relative Strength vs SPY.
    lookback ≈ 22 Handelstage ≈ 1 Monat
    """
    if BENCHMARK not in closes.columns:
        raise ValueError("SPY Benchmark fehlt in den Daten")

    # Letzte N Handelstage
    recent = closes.tail(lookback + 5).copy()  # etwas Puffer
    recent = recent.dropna(how="all")

    spy = recent[BENCHMARK]
    
    results = []

    for group_name, group_tickers in TICKERS.items():
        for ticker, name in group_tickers.items():
            if ticker not in recent.columns:
                continue

            series = recent[ticker].dropna()
            spy_aligned = spy.reindex(series.index).dropna()
            series = series.reindex(spy_aligned.index)

            if len(series) < 10:
                continue

            # Relative Strength Ratio (rebased auf 100)
            ratio = (series / spy_aligned) * 100
            ratio = ratio / ratio.iloc[0] * 100

            # Performance
            perf_1m = (series.iloc[-1] / series.iloc[0] - 1) * 100
            spy_perf = (spy_aligned.iloc[-1] / spy_aligned.iloc[0] - 1) * 100
            rel_perf = perf_1m - spy_perf

            # Letzte 22 Werte für Sparkline (normalisiert 0-100)
            spark_data = ratio.tail(22).values
            if len(spark_data) > 0:
                spark_min, spark_max = spark_data.min(), spark_data.max()
                if spark_max > spark_min:
                    spark_norm = ((spark_data - spark_min) / (spark_max - spark_min) * 100).tolist()
                else:
                    spark_norm = [50] * len(spark_data)
            else:
                spark_norm = []

            results.append({
                "group": group_name,
                "ticker": ticker,
                "name": name,
                "rs_last": round(ratio.iloc[-1], 2),
                "rel_perf": round(rel_perf, 2),
                "perf_1m": round(perf_1m, 2),
                "sparkline": spark_norm,
                "last_price": round(series.iloc[-1], 2),
            })

    # Nach Relative Performance sortieren
    results = sorted(results, key=lambda x: x["rel_perf"], reverse=True)
    return results