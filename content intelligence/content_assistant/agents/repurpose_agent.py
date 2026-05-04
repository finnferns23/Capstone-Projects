from content_assistant.agents.base import BaseAgent
from content_assistant.schemas.content_schema import ContentRequest, ContentResponse
from content_assistant.tools.prompt_tools import enrich_prompt


class RepurposeAgent(BaseAgent):
    name = "repurpose_agent"

    async def run(self, request: ContentRequest, context: str = "", memory: str = "") -> ContentResponse:
        enriched = enrich_prompt(request.prompt, request.audience, request.tone)
        if context:
            enriched += f"\nRelevant Knowledge:\n{context}"
        if memory:
            enriched += f"\nRecent Memory:\n{memory}"
        body = f"""Repurposing System
        
        Source Idea:
        {request.prompt}
        
        Repurposed Assets:
        1. Long-form blog outline
        2. LinkedIn thought leadership post
        3. Email newsletter
        4. Short video script
        5. Podcast intro script
        6. Image prompt pack
        
        Core Draft:
        {await self.llm.generate(enriched)}"""
        return ContentResponse(content=body, agent_name=self.name, mode=self.llm.mode)
