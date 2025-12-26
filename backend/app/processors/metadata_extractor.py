import re

def extract_title(soup):
    if soup.title:
        return soup.title.get_text(strip=True)
    h1 = soup.find("h1")
    return h1.get_text(strip=True) if h1 else None

def extract_dates(text: str):
    date_pattern = r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}"
    dates = re.findall(date_pattern, text)
    return dates[:2] if dates else (None, None)