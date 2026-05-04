"""LLM gateway with OpenAI support and reliable local fallback."""
from __future__ import annotations

from content_assistant.config import settings
from content_assistant.utils.logging_config import get_logger

logger = get_logger(__name__)


class LLMService:
    """Generate text through OpenAI when available, otherwise use deterministic fallback."""

    def __init__(self) -> None:
        self.mode = "openai" if settings.has_openai else "local_fallback"

    async def generate(self, prompt: str) -> str:
        """Generate a response without crashing when external services fail."""
        if self.mode == "openai":
            return await self._generate_openai(prompt)
        logger.info("Using local fallback LLM mode because OPENAI_API_KEY is not configured.")
        return self._generate_local(prompt)

    async def _generate_openai(self, prompt: str) -> str:
        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=settings.openai_api_key)
            response = await client.chat.completions.create(
                model=settings.openai_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            return response.choices[0].message.content or ""
        except Exception as exc:  # external API failures must not break local execution
            logger.exception("OpenAI generation failed. Falling back to local generation.")
            fallback = self._generate_local(prompt)
            return f"Local fallback activated because OpenAI generation failed: {exc}\n\n{fallback}"

    def _generate_local(self, prompt: str) -> str:
        return (
            "Structured local generation based on:\n"
            f"{prompt}\n\n"
            "This output is deterministic and API-free. Add API keys for model-powered generation."
        )
