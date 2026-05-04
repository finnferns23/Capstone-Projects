"""RAG service with safe failure behavior."""
from __future__ import annotations

from content_assistant.rag.retriever import RagRetriever
from content_assistant.utils.logging_config import get_logger

logger = get_logger(__name__)


class RagService:
    """Provide contextual knowledge for generation."""

    def __init__(self) -> None:
        self.retriever = RagRetriever()

    async def context_for(self, query: str) -> str:
        try:
            results = await self.retriever.retrieve(query)
            if isinstance(results, list):
                return "\n".join(str(item) for item in results if item)
            return str(results or "")
        except Exception:
            logger.exception("RAG retrieval failed. Continuing without RAG context.")
            return ""
