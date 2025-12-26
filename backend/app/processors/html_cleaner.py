from bs4 import BeautifulSoup


NOISE_TAGS = [
    "script", "style", "noscript", "iframe",
    "svg", "canvas", "footer", "header"
]


def clean_html(html: str) -> BeautifulSoup:
    soup = BeautifulSoup(html, "html.parser")

    for tag in NOISE_TAGS:
        for el in soup.find_all(tag):
            el.decompose()

    return soup
