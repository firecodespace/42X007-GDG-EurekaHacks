# backend/app/services/scraper_service.py

import time
import logging
from typing import Optional
import requests
from requests.adapters import HTTPAdapter, Retry

from playwright.sync_api import sync_playwright

LOG = logging.getLogger("scraper_service")
LOG.setLevel(logging.INFO)


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "no-cache",
}

# -------------------------------------------------------------------
# REQUESTS SESSION
# -------------------------------------------------------------------
def create_session(timeout: int = 10, max_retries: int = 3, backoff: float = 0.3) -> requests.Session:
    session = requests.Session()

    retries = Retry(
        total=max_retries,
        backoff_factor=backoff,
        status_forcelist=[403, 429, 500, 502, 503, 504],
        allowed_methods=["GET", "HEAD", "OPTIONS"],
        raise_on_status=False
    )

    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update(DEFAULT_HEADERS)

    return session


# -------------------------------------------------------------------
# PLAYWRIGHT FETCH — REAL CHROME PROFILE
# -------------------------------------------------------------------
def fetch_html_playwright(url: str, timeout: int = 25000) -> Optional[str]:
    """
    Real Chrome profile scraping.
    Avoids Cloudflare blocks, preserves cookies, acts like a real user.
    """

    LOG.info(f"[playwright] Fetching (real Chrome): {url}")

    chrome_profile = "/Users/yashbendresh/Library/Application Support/Google/Chrome/Default"

    try:
        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(
                user_data_dir=chrome_profile,
                channel="chrome",
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--start-maximized",
                    "--no-sandbox",
                    "--disable-gpu",
                ],
            )

            page = context.new_page()
            page.set_default_timeout(timeout)

            page.goto(url, wait_until="domcontentloaded")

            # ----------------------------------------------------------------
            # SMART WAITING BASED ON PAGE TYPE
            # ----------------------------------------------------------------
            if "/events/" in url:        # MLH detail pages
                try:
                    page.wait_for_selector("h1", timeout=8000)
                except:
                    page.wait_for_timeout(6000)

            elif "/hackathons" in url:   # Devpost list
                try:
                    page.wait_for_selector(".hackathon-tile", timeout=8000)
                except:
                    page.wait_for_timeout(6000)

            else:
                page.wait_for_timeout(3000)

            html = page.content()
            context.close()
            return html

    except Exception as e:
        LOG.warning(f"[playwright] Failed fetching {url}: {e}")
        return None


# -------------------------------------------------------------------
# REQUESTS FETCH
# -------------------------------------------------------------------
def fetch_html_requests(url: str, timeout: int = 10) -> Optional[str]:
    try:
        session = create_session(timeout)
        LOG.info(f"[requests] Fetching {url}")

        resp = session.get(url, timeout=timeout)

        if resp.status_code == 403:
            LOG.warning(f"[requests] 403 Forbidden: {url}")
            return None

        resp.raise_for_status()
        return resp.text

    except Exception as e:
        LOG.warning(f"[requests] Failed {url}: {e}")
        return None


# -------------------------------------------------------------------
# UNIFIED FETCHER
# -------------------------------------------------------------------
def fetch_html(url: str, timeout: int = 10, force_browser: bool = False) -> Optional[str]:
    """
    - If force_browser=True → always use Playwright 
    - Otherwise → try requests first, fallback to Playwright 
    """
    if force_browser:
        return fetch_html_playwright(url)

    html = fetch_html_requests(url, timeout)
    if html:
        return html

    LOG.info(f"[fetch_html] Falling back → Playwright: {url}")
    return fetch_html_playwright(url)
