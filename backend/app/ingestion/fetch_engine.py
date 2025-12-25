import requests

def fetch(url: str, timeout=10):
    try:
        r = requests.get(url, timeout=timeout, headers={
            "User-Agent": "Mozilla/5.0"
        })
        if r.status_code == 200:
            return r.text
        return None
    except Exception:
        return None
