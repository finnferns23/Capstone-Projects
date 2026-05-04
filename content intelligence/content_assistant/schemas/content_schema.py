from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ContentRequest:
    task: str
    prompt: str
    audience: str = "general audience"
    tone: str = "professional"
    channels: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContentResponse:
    content: str
    agent_name: str
    mode: str = "local_fallback"
    citations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
