from pathlib import Path
from datetime import date


def get_run_dir(source: str) -> Path:
    """
    Returns a guaranteed-existing directory:
    data/raw/<source>/<YYYY-MM-DD>/
    """
    today = date.today().isoformat()
    base = Path("data") / "raw" / source / today
    base.mkdir(parents=True, exist_ok=True)
    return base
