# app/ingestion/render_engine.py

import logging
from playwright.sync_api import sync_playwright

LOG = logging.getLogger("render_engine")

def render(url: str, timeout: int = 20000) -> str | None:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                channel="chrome",
                headless=False,
                args=["--disable-blink-features=AutomationControlled"]
            )
            page = browser.new_page()
            page.set_default_timeout(timeout)
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(4000)

            html = page.content()
            browser.close()
            return html

    except Exception as e:
        LOG.warning(f"[render_engine] {url} failed: {e}")
        return None
