from playwright.sync_api import sync_playwright

_browser = None

def get_browser():
    global _browser
    if _browser is None:
        p = sync_playwright().start()
        _browser = p.chromium.launch(headless=True)
    return _browser

def render(url: str, timeout=20000):
    try:
        browser = get_browser()
        page = browser.new_page()
        page.goto(url, timeout=timeout, wait_until="domcontentloaded")
        html = page.content()
        page.close()
        return html
    except Exception:
        return None
