"""Content optimization layer for capstone-grade generation output."""
from __future__ import annotations

from content_assistant.evaluation.metrics import content_quality_score


class ContentOptimizer:
    """Add practical optimization guidance to generated content."""

    def optimize(self, content: str, category: str, audience: str, tone: str) -> tuple[str, dict[str, object]]:
        quality = content_quality_score(content)
        suggestions = [
            f"Align the final message with a {tone} tone for {audience}.",
            f"Use category-specific hooks for {category} content.",
            "Close with one clear next action.",
        ]
        notes = "\n".join(f"- {item}" for item in suggestions)
        optimized = (
            f"{content.strip()}\n\n"
            "---\n"
            "Optimization Notes:\n"
            f"- Predicted content category: {category}\n"
            f"- Quality score: {quality}\n"
            f"{notes}"
        )
        return optimized, {"quality_score": quality, "optimization_suggestions": suggestions}
