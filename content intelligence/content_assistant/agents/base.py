from abc import ABC, abstractmethod
from content_assistant.schemas.content_schema import ContentRequest, ContentResponse
from content_assistant.services.llm_service import LLMService
from content_assistant.tools.content_tools import ContentToolkit


class BaseAgent(ABC):
    name = "base_agent"

    def __init__(self, llm: LLMService | None = None) -> None:
        self.llm = llm or LLMService()
        self.tools = ContentToolkit()

    @abstractmethod
    async def run(self, request: ContentRequest, context: str = "", memory: str = "") -> ContentResponse:
        raise NotImplementedError
