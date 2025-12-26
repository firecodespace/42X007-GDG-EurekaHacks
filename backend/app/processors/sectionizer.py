import re


SECTION_HEADERS = [
    "Dates",
    "Eligibility",
    "Rules",
    "Prizes",
    "Judging",
    "How To Enter",
    "Submission",
    "Schedule",
    "Sponsors",
    "Contact",
]


def split_sections(text: str) -> dict:
    """
    Splits long event text into logical sections using heuristic headers.
    """
    sections = {}
    current_section = "Overview"
    sections[current_section] = []

    lines = text.splitlines()

    for line in lines:
        clean = line.strip()
        if not clean:
            continue

        header_match = next(
            (h for h in SECTION_HEADERS if h.lower() in clean.lower()),
            None,
        )

        if header_match:
            current_section = header_match
            sections[current_section] = []
        else:
            sections[current_section].append(clean)

    return {
        section: "\n".join(content)
        for section, content in sections.items()
        if content
    }
