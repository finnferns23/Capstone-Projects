def truncate(text: str, limit: int = 500) -> str:
    return text if len(text) <= limit else text[: limit - 3] + "..."


def clean_text(text: str) -> str:
    return " ".join(text.split())
