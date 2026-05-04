"""Capstone intelligence service combining datasets, ML classification, and analytics."""
from __future__ import annotations

from typing import Dict, List

from content_assistant.analytics.usage_tracker import UsageTracker
from content_assistant.config import settings
from content_assistant.data_pipeline.data_cleaner import build_training_columns
from content_assistant.data_pipeline.data_loader import dataset_profile, load_many, load_many_frames
from content_assistant.evaluation.metrics import label_distribution
from content_assistant.models.content_classifier import ContentClassifier
from content_assistant.services.content_optimizer import ContentOptimizer
from content_assistant.utils.logging_config import get_logger

logger = get_logger(__name__)


class CapstoneIntelligenceService:
    """Load datasets, train the classifier, optimize output, and track usage."""

    def __init__(self) -> None:
        self.classifier = ContentClassifier()
        self.optimizer = ContentOptimizer()
        self.tracker = UsageTracker()
        self.dataset_rows: List[Dict[str, str]] = []
        self.dataset_summary: dict[str, object] = {}
        self._prepare_classifier()

    def _prepare_classifier(self) -> None:
        dataset_dir = settings.base_dir / "data" / "datasets"
        paths = sorted(dataset_dir.glob("*.csv"))
        if not paths:
            logger.warning("No datasets found for classifier training; using rule-based fallback.")
            return
        try:
            frame = load_many_frames(paths)
            self.dataset_summary = dataset_profile(frame)
            self.dataset_rows = load_many(paths)
            texts, labels = build_training_columns(self.dataset_rows)
            self.classifier.train(texts, labels)
            self.dataset_summary["label_distribution"] = label_distribution(labels)
            logger.info("Classifier prepared with %s rows and labels=%s.", len(texts), sorted(set(labels)))
        except Exception:
            logger.exception("Dataset-driven classifier failed; using rule-based fallback.")

    def classify(self, prompt: str) -> str:
        return self.classifier.predict(prompt)

    def confidence(self, prompt: str) -> dict[str, float]:
        return self.classifier.predict_proba(prompt)

    def optimize(self, content: str, category: str, audience: str, tone: str) -> tuple[str, dict[str, object]]:
        optimized, metadata = self.optimizer.optimize(content, category=category, audience=audience, tone=tone)
        metadata["dataset_summary"] = self.dataset_summary
        return optimized, metadata

    def track(self, event: Dict[str, object]) -> None:
        try:
            self.tracker.track(event)
        except Exception:
            logger.exception("Usage tracking failed; continuing without blocking workflow.")
