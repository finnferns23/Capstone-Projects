"""Persistent JSON memory store with backward-compatible loading."""
from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, List


class JsonMemory:
    """Small local JSON memory store for prompts and response previews."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text(json.dumps({"items": []}, indent=2), encoding="utf-8")

    def load(self) -> Dict[str, Any]:
        """Load memory and normalize older list-based files."""
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            payload = {"items": []}
        if isinstance(payload, list):
            payload = {"items": payload}
        if not isinstance(payload, dict):
            payload = {"items": []}
        payload.setdefault("items", [])
        return payload

    def add(self, prompt: str, response: str, task: str) -> None:
        data = self.load()
        data.setdefault("items", []).append(
            {
                "timestamp": datetime.now(UTC).isoformat(),
                "task": task,
                "prompt": prompt,
                "response_preview": response[:500],
            }
        )
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def recent(self, limit: int = 3) -> List[Dict[str, Any]]:
        return self.load().get("items", [])[-limit:]
