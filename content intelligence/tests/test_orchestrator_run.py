"""Runtime smoke test for the production assistant workflow."""
from __future__ import annotations

import asyncio

from content_assistant.orchestrator import ContentAssistantOrchestrator
from content_assistant.schemas.content_schema import ContentRequest


def test_orchestrator_returns_content() -> None:
    orchestrator = ContentAssistantOrchestrator()
    request = ContentRequest(task="text", prompt="Create a short launch message.")
    response = asyncio.run(orchestrator.run(request))

    assert response.content
    assert response.agent_name
    assert response.mode in {"local_fallback", "openai", "safe_error_fallback"}
