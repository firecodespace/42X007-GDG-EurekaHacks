import requests
from bs4 import BeautifulSoup

def fetch_html(url: str):
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")
