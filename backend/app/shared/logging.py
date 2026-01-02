import logging


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure global logging for the application.
    Call this once at startup.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
