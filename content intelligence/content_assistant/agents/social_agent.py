from content_assistant.agents.base import BaseAgent
from content_assistant.schemas.content_schema import ContentRequest, ContentResponse
from content_assistant.tools.prompt_tools import enrich_prompt


class SocialAgent(BaseAgent):
    name = "social_agent"

    async def run(self, request: ContentRequest, context: str = "", memory: str = "") -> ContentResponse:
        enriched = enrich_prompt(request.prompt, request.audience, request.tone)
        if context:
            enriched += f"\nRelevant Knowledge:\n{context}"
        if memory:
            enriched += f"\nRecent Memory:\n{memory}"
        body = f"""Social Content Pack
        
        LinkedIn Post:
        {await self.llm.generate(enriched)}
        
        X Post:
        A concise hook for {request.audience}: {request.prompt}
        
        Instagram Caption:
        Make the idea visual, useful, and easy to save.
        
        CTA:
        {self.tools.cta('social')}"""
        return ContentResponse(content=body, agent_name=self.name, mode=self.llm.mode)
