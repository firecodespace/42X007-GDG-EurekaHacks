from bs4 import BeautifulSoup


def extract_title(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    selectors = [
        "h1",
        "meta[property='og:title']",
        "title",
    ]

    for sel in selectors:
        el = soup.select_one(sel)
        if not el:
            continue

        if el.name == "meta":
            return (el.get("content") or "").strip()

        return el.get_text(strip=True)

    return ""
