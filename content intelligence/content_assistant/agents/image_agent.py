from content_assistant.agents.base import BaseAgent
from content_assistant.schemas.content_schema import ContentRequest, ContentResponse
from content_assistant.tools.prompt_tools import enrich_prompt


class ImageAgent(BaseAgent):
    name = "image_agent"

    async def run(self, request: ContentRequest, context: str = "", memory: str = "") -> ContentResponse:
        enriched = enrich_prompt(request.prompt, request.audience, request.tone)
        if context:
            enriched += f"\nRelevant Knowledge:\n{context}"
        if memory:
            enriched += f"\nRecent Memory:\n{memory}"
        body = f"""Image Generation Brief
        
        Primary Prompt:
        {self.tools.image_prompt(request.prompt, request.tone)}
        
        Creative Direction:
        Design for {request.audience}. Keep it polished, clear, and brand-safe.
        
        Variants:
        1. Premium editorial visual
        2. Social media hero graphic
        3. Product-style feature visual"""
        return ContentResponse(content=body, agent_name=self.name, mode=self.llm.mode)
