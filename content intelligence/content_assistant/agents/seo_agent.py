from content_assistant.agents.base import BaseAgent
from content_assistant.schemas.content_schema import ContentRequest, ContentResponse
from content_assistant.tools.prompt_tools import enrich_prompt


class SeoAgent(BaseAgent):
    name = "seo_agent"

    async def run(self, request: ContentRequest, context: str = "", memory: str = "") -> ContentResponse:
        enriched = enrich_prompt(request.prompt, request.audience, request.tone)
        if context:
            enriched += f"\nRelevant Knowledge:\n{context}"
        if memory:
            enriched += f"\nRecent Memory:\n{memory}"
        keywords = "\n".join(f"- {word}" for word in self.tools.keywords(request.prompt))
        body = f"""SEO Content Plan
        
        Meta Description:
        {self.tools.meta(request.prompt)}
        
        Keyword Pack:
        {keywords}
        
        Search Intent:
        Informational and commercial investigation.
        
        Recommended Structure:
        {await self.llm.generate(enriched)}"""
        return ContentResponse(content=body, agent_name=self.name, mode=self.llm.mode)
