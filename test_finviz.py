import os
import requests

API_KEY = os.getenv("FINVIZ_API_KEY") or "DEIN_KEY_HIER"

# Test 1: Einfacher Export-Versuch
url = "https://elite.finviz.com/export.ashx"
params = {
    "v": "111",          # Overview
    "t": "SPY,XBI,QQQE",
    "auth": API_KEY
}

response = requests.get(url, params=params)
print("Status Code:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))
print("\nErste 500 Zeichen der Antwort:")
print(response.text[:500])
