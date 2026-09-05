import csv
import io
import os
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import requests

# Export-URLs ohne auth= — Token kommt aus FINVIZ_API_KEY.
SCREENER_URLS = {
    "jahr": os.getenv(
        "FINVIZ_URL_JAHR",
        "https://elite.finviz.com/export/screener?v=111&f=cap_10to,ind_stocksonly,sh_float_150tox,ta_perf_10y50o,ta_perf2_52w50o&o=-marketcap",
    ),
    "quartal": os.getenv(
        "FINVIZ_URL_QUARTAL",
        "https://elite.finviz.com/export/screener?v=111&f=cap_10to,ind_stocksonly,sh_float_150tox,ta_perf_10y50o,ta_perf2_50to-26w&o=-marketcap",
    ),
    "monat": os.getenv(
        "FINVIZ_URL_MONAT",
        "https://elite.finviz.com/export/screener?v=111&f=cap_7to,sh_avgvol_o300,sh_curvol_o100,ta_perf_26w50o,ta_volatility_mo5&o=-perf4w",
    ),
    "woche": os.getenv(
        "FINVIZ_URL_WOCHE",
        "https://elite.finviz.com/export/screener?v=111&f=cap_7to,sh_avgvol_o300,sh_curvol_o100,ta_perf_1w10o,ta_volatility_wo4&o=-marketcap",
    ),
    "volume": os.getenv(
        "FINVIZ_URL_VOLUME",
        "https://elite.finviz.com/export/screener?v=111&f=cap_midover,ind_stocksonly,sh_relvol_o1.5,ta_perf_7.5to-d,ta_perf2_20to-4w",
    ),
}

COLUMNS = ("jahr", "quartal", "monat", "woche", "volume")
HEADERS = {"User-Agent": "Mozilla/5.0"}


def _auth() -> str:
    return (os.getenv("FINVIZ_API_KEY") or "").strip()


def to_export_url(url: str, auth: str) -> str:
    # Filter unverändert lassen, nur auth anhängen.
    raw = url.strip()
    if "auth=" in raw:
        p = urlparse(raw)
        q = parse_qs(p.query, keep_blank_values=True)
        q.pop("auth", None)
        raw = urlunparse((p.scheme, p.netloc, p.path, p.params,
                          urlencode({k: v[-1] for k, v in q.items()}, safe=","),
                          p.fragment))
    sep = "&" if "?" in raw else "?"
    return f"{raw}{sep}auth={auth}"


def tickers_from_csv(text: str) -> list[str]:
    sample = text.lstrip()
    if sample.lower().startswith("<!doctype") or sample.lower().startswith("<html"):
        raise RuntimeError("Finviz lieferte HTML statt CSV (Token?)")
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        return []
    key = next(
        (c for c in reader.fieldnames if c.strip().lower() in {"ticker", "symbol", "t"}),
        reader.fieldnames[0],
    )
    out = []
    for row in reader:
        t = (row.get(key) or "").strip().upper()
        if t:
            out.append(t)
    return out


def fetch_screener_tickers(url: str, auth: str) -> list[str]:
    if not url:
        return []
    export_url = to_export_url(url, auth)
    print(f"Finviz GET {export_url.split('auth=')[0]}auth=***")
    r = requests.get(export_url, headers=HEADERS, timeout=45)
    print(f"Finviz HTTP {r.status_code} {r.headers.get('Content-Type')} {len(r.content)}b | {r.text[:120]!r}")
    r.raise_for_status()
    return tickers_from_csv(r.text)


def combined_screener_url(tickers: list[str]) -> str:
    if not tickers:
        return ""
    return (
        "https://elite.finviz.com/screener?v=211&p=d&t="
        + ",".join(tickers)
        + "&ta=0&o=-perf4w"
    )


def to_browser_url(url: str) -> str:
    """Export-URL → normale Screener-URL zum Öffnen im Browser."""
    if not url:
        return ""
    p = urlparse(url)
    q = parse_qs(p.query, keep_blank_values=True)
    q.pop("auth", None)
    query = urlencode({k: v[-1] for k, v in q.items()})
    return urlunparse(("https", "elite.finviz.com", "/screener.ashx", "", query, ""))


def load_screening() -> dict:
    auth = _auth()
    sets: dict[str, set[str]] = {k: set() for k in COLUMNS}
    errors: list[str] = []

    if not auth:
        errors.append("FINVIZ_API_KEY fehlt")
    else:
        for key in COLUMNS:
            url = SCREENER_URLS.get(key) or ""
            if not url:
                errors.append(f"{key}: URL leer")
                continue
            try:
                got = fetch_screener_tickers(url, auth)
                sets[key] = set(got)
                print(f"Finviz {key}: {len(got)} Ticker")
            except Exception as e:
                errors.append(f"{key}: {e}")
                print(f"Finviz {key} Fehler: {e}")

    all_tickers = sorted(set().union(*sets.values()))
    rows = []
    for t in all_tickers:
        row = {
            "ticker": t,
            "jahr": 1 if t in sets["jahr"] else 0,
            "quartal": 1 if t in sets["quartal"] else 0,
            "monat": 1 if t in sets["monat"] else 0,
            "woche": 1 if t in sets["woche"] else 0,
            "volume": 1 if t in sets["volume"] else 0,
        }
        row["total"] = (
            row["jahr"] + row["quartal"] + row["monat"] + row["woche"] + row["volume"]
        )
        rows.append(row)

    rows.sort(key=lambda r: (-r["total"], r["ticker"]))
    uniq = [r["ticker"] for r in rows]

    return {
        "rows": rows,
        "screener_url": combined_screener_url(uniq) if uniq else "",
        "count": len(uniq),
        "errors": errors,
        "counts": {k: len(sets[k]) for k in COLUMNS},
        "header_urls": {
            k: combined_screener_url(sorted(sets[k])) for k in COLUMNS
        },
    }