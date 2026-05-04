from content_assistant.agents.base import BaseAgent
from content_assistant.schemas.content_schema import ContentRequest, ContentResponse
from content_assistant.tools.prompt_tools import enrich_prompt


class TextAgent(BaseAgent):
    name = "text_agent"

    async def run(self, request: ContentRequest, context: str = "", memory: str = "") -> ContentResponse:
        enriched = enrich_prompt(request.prompt, request.audience, request.tone)
        if context:
            enriched += f"\nRelevant Knowledge:\n{context}"
        if memory:
            enriched += f"\nRecent Memory:\n{memory}"
        body = f"""{self.tools.headline(request.prompt, request.audience)}
        
        Summary:
        Create clear, useful, channel-ready content for {request.audience} in a {request.tone} tone.
        
        Draft:
        {await self.llm.generate(enriched)}
        
        Call to Action:
        {self.tools.cta(request.task)}"""
        return ContentResponse(content=body, agent_name=self.name, mode=self.llm.mode)
