# TEST: nur 1 Ticker + SPY, damit Railway schnell startet.
# Vollen Katalog aus Git-History zurückholen, sobald Screening steht.

TICKERS = {
    "sectors": {
        "USO": "Oil",
    },
    "equal_weight": {},
    "countries": {},
}

BENCHMARK = "SPY"
ALL_TICKERS = (
    list(TICKERS["sectors"].keys())
    + list(TICKERS["equal_weight"].keys())
    + list(TICKERS["countries"].keys())
    + [BENCHMARK]
)