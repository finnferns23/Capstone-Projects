from content_assistant.agents.base import BaseAgent
from content_assistant.schemas.content_schema import ContentRequest, ContentResponse
from content_assistant.tools.prompt_tools import enrich_prompt


class BlogAgent(BaseAgent):
    name = "blog_agent"

    async def run(self, request: ContentRequest, context: str = "", memory: str = "") -> ContentResponse:
        enriched = enrich_prompt(request.prompt, request.audience, request.tone)
        if context:
            enriched += f"\nRelevant Knowledge:\n{context}"
        if memory:
            enriched += f"\nRecent Memory:\n{memory}"
        keywords = ", ".join(self.tools.keywords(request.prompt))
        body = f"""# {self.tools.headline(request.prompt, request.audience)}
        
        Meta Description: {self.tools.meta(request.prompt)}
        
        Target Keywords: {keywords}
        
        Introduction:
        {await self.llm.generate(enriched)}
        
        Structure:
        1. Problem and audience pain point
        2. Solution framework
        3. Practical examples
        4. Action checklist
        5. Conversion-focused conclusion"""
        return ContentResponse(content=body, agent_name=self.name, mode=self.llm.mode)
