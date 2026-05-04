from content_assistant.agents.base import BaseAgent
from content_assistant.schemas.content_schema import ContentRequest, ContentResponse
from content_assistant.tools.prompt_tools import enrich_prompt


class AudioAgent(BaseAgent):
    name = "audio_agent"

    async def run(self, request: ContentRequest, context: str = "", memory: str = "") -> ContentResponse:
        enriched = enrich_prompt(request.prompt, request.audience, request.tone)
        if context:
            enriched += f"\nRelevant Knowledge:\n{context}"
        if memory:
            enriched += f"\nRecent Memory:\n{memory}"
        body = f"""Audio Script
        
        Opening Hook:
        Here is why this matters to {request.audience}.
        
        Narration:
        {await self.llm.generate(enriched)}
        
        Voice Direction:
        Tone should be {request.tone}, clear, warm, and confident.
        
        Production Note:
        Use ElevenLabs integration when ELEVENLABS_API_KEY is configured."""
        return ContentResponse(content=body, agent_name=self.name, mode=self.llm.mode)
