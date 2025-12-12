# backend/app/scrapers/run_crawler.py

import json
import os
from app.engine.crawler import Crawler

def main():
    crawler = Crawler(delay=0.4)

    seeds = [
        "https://mlh.io/seasons/2025/events",
        "https://devpost.com/hackathons",
        "https://unstop.com/competitions",
    ]

    # allowed domains list used per crawl (keeps crawler domain-bounded)
    domain_map = {
        "https://mlh.io/seasons/2025/events": ["mlh.io"],
        "https://devpost.com/hackathons": ["devpost.com"],
        "https://unstop.com/competitions": ["unstop.com"],
    }

    competitions = []

    for seed in seeds:
        allowed = domain_map.get(seed, None)
        scraped = crawler.crawl(start_url=seed, allowed_domains=allowed, max_pages=200)
        if scraped:
            competitions.extend(scraped)

    print(f"\nTotal competitions scraped: {len(competitions)}")

    out_dir = "public/mock"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "all_competitions.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(competitions, f, indent=2, ensure_ascii=False)

    print(f"Saved → {out_path}")


if __name__ == "__main__":
    main()
