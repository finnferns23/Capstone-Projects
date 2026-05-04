"""CLI entry point for the Advanced Content AI Assistant."""
from __future__ import annotations

import argparse
import asyncio
from content_assistant.orchestrator import ContentAssistantOrchestrator
from content_assistant.schemas.content_schema import ContentRequest
from content_assistant.utils.logging_config import get_logger

logger = get_logger(__name__)


async def run_cli() -> None:
    parser = argparse.ArgumentParser(description="Advanced Content AI Assistant CLI")
    parser.add_argument("--task", default="campaign", help="Task: text, blog, social, email, audio, video, image, campaign, repurpose, seo")
    parser.add_argument("--prompt", default="Create a launch campaign for an AI productivity assistant", help="User content request")
    parser.add_argument("--audience", default="general audience", help="Target audience")
    parser.add_argument("--tone", default="professional", help="Output tone")
    args = parser.parse_args()

    try:
        orchestrator = ContentAssistantOrchestrator()
        request = ContentRequest(task=args.task, prompt=args.prompt, audience=args.audience, tone=args.tone)
        response = await orchestrator.run(request)
        print("\n=== AI Content Intelligence Capstone Output ===\n")
        print(response.content)
        print(f"\nAgent: {response.agent_name} | Mode: {response.mode}")
        if response.metadata.get("saved_path"):
            print(f"Saved: {response.metadata['saved_path']}")
    except Exception as exc:
        logger.exception("CLI execution failed.")
        raise SystemExit(f"CLI execution failed: {exc}") from exc


if __name__ == "__main__":
    asyncio.run(run_cli())
