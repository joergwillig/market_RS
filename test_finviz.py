import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("FINVIZ_API_KEY")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/csv,application/csv,text/plain",
    "Accept-Language": "en-US,en;q=0.9",
}

url = "https://elite.finviz.com/export.ashx"
params = {
    "v": "111",
    "t": "SPY,XBI,QQQE",
    "auth": API_KEY
}

response = requests.get(url, params=params, headers=headers)

print("Status Code:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))
print("\nErste 500 Zeichen:")
print(response.text[:500])