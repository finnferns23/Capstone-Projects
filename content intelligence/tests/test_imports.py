import asyncio
from content_assistant.orchestrator import ContentAssistantOrchestrator
from content_assistant.schemas.content_schema import ContentRequest


def test_orchestrator_runs() -> None:
    async def _run() -> None:
        orchestrator = ContentAssistantOrchestrator()
        response = await orchestrator.run(ContentRequest(task="text", prompt="Create a test content plan"))
        assert response.content
        assert response.agent_name

    asyncio.run(_run())
