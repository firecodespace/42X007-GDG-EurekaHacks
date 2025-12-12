from app.services.scraper_service import fetch_html

def scrape_gdg_events():
    url = "https://gdg.community.dev/events/"
    soup = fetch_html(url)

    events = []

    for card in soup.select(".event-card"):
        events.append({
            "title": card.select_one(".event-card__title").get_text(strip=True),
            "link": card.select_one("a")["href"],
            "date": card.select_one(".event-card__date").get_text(strip=True),
            "location": "Online or In-Person",
            "source": "GDG",
        })

    return events
