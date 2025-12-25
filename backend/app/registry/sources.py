# app/registry/sources.py

ALL_SOURCES = [
    {
        "name": "MLH",
        "seed": "https://mlh.io/seasons/2025/events",
        "domains": ["mlh.io", "events.mlh.io"],
        "fetch_mode": "browser"   # 👈 IMPORTANT
    },
    {
        "name": "Devpost",
        "seed": "https://devpost.com/hackathons",
        "domains": ["devpost.com"],
        "fetch_mode": "http"
    },
    {
        "name": "Unstop",
        "seed": "https://unstop.com/hackathons",
        "domains": ["unstop.com"],
        "fetch_mode": "http"
    }
]
