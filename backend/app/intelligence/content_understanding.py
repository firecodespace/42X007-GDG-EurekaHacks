# app/intelligence/content_understanding.py

def build_llm_prompt(user: dict, events: list[dict]) -> dict:
    return {
        "user_profile": user,
        "events": events,
        "task": (
            "Rank events by relevance, explain why each fits the user, "
            "and output UI-ready JSON."
        )
    }
