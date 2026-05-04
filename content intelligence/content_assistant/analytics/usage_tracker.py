"""Usage analytics tracking for portfolio and capstone reporting."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import pandas as pd

from content_assistant.config import settings


class UsageTracker:
    """Append-only JSONL tracker with pandas summary helpers."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or settings.output_dir / "usage_events.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def track(self, event: Dict[str, object]) -> None:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **event,
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def load_events(self) -> List[Dict[str, object]]:
        if not self.path.exists():
            return []
        events: List[Dict[str, object]] = []
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    events.append(json.loads(line))
        return events

    def summary(self) -> dict[str, object]:
        events = self.load_events()
        if not events:
            return {"events": 0, "top_tasks": {}, "average_quality_score": 0.0}
        frame = pd.DataFrame(events)
        quality = pd.to_numeric(frame.get("quality_score", pd.Series(dtype=float)), errors="coerce")
        return {
            "events": int(len(frame)),
            "top_tasks": frame.get("task", pd.Series(dtype=str)).value_counts().head(5).to_dict(),
            "average_quality_score": round(float(quality.dropna().mean()), 4) if not quality.dropna().empty else 0.0,
        }
