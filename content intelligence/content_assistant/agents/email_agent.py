from content_assistant.agents.base import BaseAgent
from content_assistant.schemas.content_schema import ContentRequest, ContentResponse
from content_assistant.tools.prompt_tools import enrich_prompt


class EmailAgent(BaseAgent):
    name = "email_agent"

    async def run(self, request: ContentRequest, context: str = "", memory: str = "") -> ContentResponse:
        enriched = enrich_prompt(request.prompt, request.audience, request.tone)
        if context:
            enriched += f"\nRelevant Knowledge:\n{context}"
        if memory:
            enriched += f"\nRecent Memory:\n{memory}"
        body = f"""Subject: A better way to approach {request.prompt[:48]}
        
        Hi there,
        
        {await self.llm.generate(enriched)}
        
        Best next step:
        {self.tools.cta('email')}"""
        return ContentResponse(content=body, agent_name=self.name, mode=self.llm.mode)
