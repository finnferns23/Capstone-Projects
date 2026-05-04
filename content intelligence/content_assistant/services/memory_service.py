"""Unified memory service for JSON and vector-backed recall."""
from __future__ import annotations

from content_assistant.config import settings
from content_assistant.memory.json_memory import JsonMemory
from content_assistant.memory.vector_memory import VectorMemory
from content_assistant.utils.logging_config import get_logger

logger = get_logger(__name__)


class MemoryService:
    """Coordinates persistent JSON memory and optional vector memory."""

    def __init__(self) -> None:
        self.json_memory = JsonMemory(settings.memory_path)
        self.vector_memory = VectorMemory()

    async def recall(self, query: str) -> str:
        try:
            recent_items = self.json_memory.recent(limit=3)
            recent = "\n".join(
                f"Task: {item.get('task', '')} | Prompt: {item.get('prompt', '')} | Response: {item.get('response_preview', '')}"
                for item in recent_items
            )
            semantic_items = await self.vector_memory.search(query)
            semantic = "\n".join(str(item) for item in semantic_items)
            return "\n".join(part for part in [recent, semantic] if part).strip()
        except Exception:
            logger.exception("Memory recall failed. Returning empty memory context.")
            return ""

    async def remember(self, prompt: str, response: str, task: str) -> None:
        try:
            self.json_memory.add(prompt=prompt, response=response, task=task)
            await self.vector_memory.add_text(text=f"Task: {task}\nPrompt: {prompt}\nResponse: {response}")
        except Exception:
            logger.exception("Memory persistence failed.")
            raise
