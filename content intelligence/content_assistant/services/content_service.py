"""Content generation service that routes requests to the correct agent."""
from __future__ import annotations

from content_assistant.core.router import AgentRouter
from content_assistant.schemas.content_schema import ContentRequest, ContentResponse
from content_assistant.utils.logging_config import get_logger

logger = get_logger(__name__)


class ContentService:
    """Route a normalized request to the matching content agent."""

    def __init__(self) -> None:
        self.router = AgentRouter()

    async def generate(self, request: ContentRequest, context: str, memory: str) -> ContentResponse:
        agent = self.router.route(request.task)
        logger.info("Selected agent=%s for task=%s", agent.name, request.task)
        return await agent.run(request, context=context, memory=memory)
