from pathlib import Path
from datetime import UTC, datetime


def save_markdown(content: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"content_output_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.md"
    path = output_dir / filename
    path.write_text(content, encoding="utf-8")
    return path
