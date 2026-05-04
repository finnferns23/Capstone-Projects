"""Application configuration with safe environment handling."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from environment variables with safe defaults."""

    base_dir: Path = Path(__file__).resolve().parent.parent
    provider: str = os.getenv("CONTENT_ASSISTANT_PROVIDER", "local").strip() or "local"
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "").strip()
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"
    elevenlabs_api_key: str = os.getenv("ELEVENLABS_API_KEY", "").strip()
    elevenlabs_voice_id: str = os.getenv("ELEVENLABS_VOICE_ID", "").strip()
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY", "").strip()
    pinecone_index_name: str = os.getenv("PINECONE_INDEX_NAME", "content-assistant").strip()
    chroma_persist_dir: Path = Path(os.getenv("CHROMA_PERSIST_DIR", "data/vector_db/chroma"))
    memory_path: Path = Path(os.getenv("CONTENT_ASSISTANT_MEMORY_PATH", "data/assistant_memory.json"))
    knowledge_base_dir: Path = Path(os.getenv("CONTENT_ASSISTANT_KB_DIR", "data/knowledge_base"))
    output_dir: Path = Path(os.getenv("CONTENT_ASSISTANT_OUTPUT_DIR", "outputs"))
    log_level: str = os.getenv("CONTENT_ASSISTANT_LOG_LEVEL", "INFO").upper()

    def ensure_directories(self) -> None:
        """Create runtime directories so CLI and Streamlit runs do not fail."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        self.knowledge_base_dir.mkdir(parents=True, exist_ok=True)
        self.chroma_persist_dir.mkdir(parents=True, exist_ok=True)

    @property
    def has_openai(self) -> bool:
        return bool(self.openai_api_key)

    @property
    def has_elevenlabs(self) -> bool:
        return bool(self.elevenlabs_api_key)

    @property
    def has_pinecone(self) -> bool:
        return bool(self.pinecone_api_key)


settings = Settings()
settings.ensure_directories()
