# app/ingestion/clean_engine.py

import trafilatura
from readability import Document

def clean(html: str) -> str:
    if not html:
        return ""

    text = trafilatura.extract(html)
    if text:
        return text.strip()

    # fallback
    readable = Document(html)
    return readable.summary(html_partial=True)
