from content_assistant.agents.base import BaseAgent
from content_assistant.schemas.content_schema import ContentRequest, ContentResponse
from content_assistant.tools.prompt_tools import enrich_prompt


class VideoAgent(BaseAgent):
    name = "video_agent"

    async def run(self, request: ContentRequest, context: str = "", memory: str = "") -> ContentResponse:
        enriched = enrich_prompt(request.prompt, request.audience, request.tone)
        if context:
            enriched += f"\nRelevant Knowledge:\n{context}"
        if memory:
            enriched += f"\nRecent Memory:\n{memory}"
        shots = "\n".join(f"- {shot}" for shot in self.tools.shots(request.prompt))
        body = f"""Video Script and Storyboard
        
        Concept:
        {await self.llm.generate(enriched)}
        
        Shot List:
        {shots}
        
        On-Screen Text:
        Use concise benefit-led captions for each scene."""
        return ContentResponse(content=body, agent_name=self.name, mode=self.llm.mode)
