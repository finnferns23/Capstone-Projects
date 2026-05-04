"""Grounding and citation helpers to reduce unsupported content claims."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class GroundingResult:
    """Grounding metadata returned with every generated answer."""

    sources: list[str]
    warning: str | None = None


class GroundingGuard:
    """Attach visible source context and fallback warnings to generated content."""

    def build(self, rag_context: str, dataset_summary: dict[str, object] | None = None) -> GroundingResult:
        sources: list[str] = []
        if rag_context.strip():
            sources.append("local_knowledge_base")
        if dataset_summary:
            rows = dataset_summary.get("rows")
            if rows:
                sources.append(f"capstone_sample_datasets:{rows}_rows")
        warning = None if sources else "No grounding source was available; output used local fallback generation."
        return GroundingResult(sources=sources, warning=warning)

    def append_note(self, content: str, grounding: GroundingResult) -> str:
        if not grounding.sources and not grounding.warning:
            return content
        lines = [content.rstrip(), "", "Grounding Notes:"]
        if grounding.sources:
            lines.append("- Sources used: " + ", ".join(grounding.sources))
        if grounding.warning:
            lines.append("- Warning: " + grounding.warning)
        return "\n".join(lines)
