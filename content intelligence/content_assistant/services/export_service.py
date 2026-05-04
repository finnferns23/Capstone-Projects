from pathlib import Path
from content_assistant.config import settings
from content_assistant.tools.export_tools import save_markdown


class ExportService:
    def save(self, content: str) -> Path:
        return save_markdown(content, settings.output_dir)
