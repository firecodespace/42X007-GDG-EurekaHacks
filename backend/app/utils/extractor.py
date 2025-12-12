from bs4 import BeautifulSoup
import re

def safe(node):
    return node.get_text(" ", strip=True) if node else ""


def extract_event_data(html: str, url: str, source: str):
    soup = BeautifulSoup(html, "html.parser")

    # =========================================================
    # TITLE
    # =========================================================
    title = safe(soup.select_one("h1")) or safe(soup.select_one(".event-title"))

    # =========================================================
    # FULL TEXT (for pattern extraction)
    # =========================================================
    full_text = safe(soup.select_one("main")) or safe(soup)

    # =========================================================
    # DEADLINE DETECTION
    # MLH dates appear like:
    # “Friday July 12, 2024 11:00AM to Jul 14, 12:00PM EST”
    # =========================================================
    date_pattern = r"[A-Za-z]+\s+[A-Za-z]+\s+\d{1,2},\s+\d{4}.*?EST"
    date_match = re.search(date_pattern, full_text)

    deadline = date_match.group(0) if date_match else ""

    # =========================================================
    # LOCATION DETECTION
    # MLH typically shows:
    #  - "Event is hosted online"
    #  - "Online"
    #  - "In Person — XYZ"
    # =========================================================
    location = ""

    if "hosted online" in full_text.lower():
        location = "Online"
    else:
        # Look for any line containing "Location"
        loc_match = re.search(r"Location[:\s]+(.+)", full_text, re.IGNORECASE)
        if loc_match:
            location = loc_match.group(1).strip()

        # Fallback: look for visible location sections
        if not location:
            possible_locs = soup.find_all(["p", "div"], string=True)
            for text in possible_locs:
                t = text.get_text(strip=True)
                if "Online" in t:
                    location = "Online"
                    break
                if "In Person" in t or "Hybrid" in t:
                    location = t
                    break

    # =========================================================
    # DESCRIPTION EXTRACTION
    # =========================================================
    desc_node = (
        soup.select_one(".markdown")
        or soup.select_one(".event-details")
        or soup.select_one("section")
        or soup.find("p")
    )

    description = safe(desc_node)

    # =========================================================
    # FINAL STRUCTURED OUTPUT
    # =========================================================
    return {
        "title": title,
        "link": url,
        "source": source,
        "location": location,
        "deadline": deadline,
        "raw_description": description,
        "tags": []   # MLH provides no tags; ignore form fields
    }
