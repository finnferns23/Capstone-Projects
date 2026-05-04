from content_assistant.agents.base import BaseAgent
from content_assistant.schemas.content_schema import ContentRequest, ContentResponse
from content_assistant.tools.prompt_tools import enrich_prompt


class CampaignAgent(BaseAgent):
    name = "campaign_agent"

    async def run(self, request: ContentRequest, context: str = "", memory: str = "") -> ContentResponse:
        enriched = enrich_prompt(request.prompt, request.audience, request.tone)
        if context:
            enriched += f"\nRelevant Knowledge:\n{context}"
        if memory:
            enriched += f"\nRecent Memory:\n{memory}"
        body = f"""Integrated Campaign Plan
        
        Campaign Idea:
        {await self.llm.generate(enriched)}
        
        Pillars:
        1. Awareness content
        2. Education content
        3. Trust-building proof
        4. Conversion offer
        
        Channels:
        - Blog
        - LinkedIn
        - Email
        - Short video
        - Audio script
        - Image prompts
        
        CTA:
        {self.tools.cta('campaign')}"""
        return ContentResponse(content=body, agent_name=self.name, mode=self.llm.mode)
