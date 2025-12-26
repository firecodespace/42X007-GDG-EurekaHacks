from app.acquisition.fetched_page import FetchedPage
from app.domain.event_source import EventSource
from app.extraction.extract_event import extract_event
from app.normalization.build_event import build_event
from app.utils.time import utc_now


def test_extraction_and_normalization():
    html = """
    <html>
    <h1>AI Innovation Hackathon</h1>
    <p>
        This is an online hackathon focused on artificial intelligence,
        machine learning, deep learning, and applied data science.
        Participants will build innovative solutions using real-world
        datasets and cutting-edge technologies. The event encourages
        collaboration, creativity, and problem-solving across domains.
        The submission deadline is March 30, 2025.
    </p>
    </html>
    """


    page = FetchedPage(
        url="https://example.com/hackathon",
        source=EventSource.DEVPOST,
        html=html,
        fetched_at=utc_now(),
    )

    raw = extract_event(page)
    event = build_event(raw)

    assert event.title == "AI Innovation Hackathon"
    assert event.location == "Online"
    assert event.deadline is not None
