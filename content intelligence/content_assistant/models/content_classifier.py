"""ML-powered content classifier for capstone-grade routing."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Iterable

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from content_assistant.data_pipeline.data_cleaner import clean_text


@dataclass
class ContentClassifier:
    """Classify prompts using TF-IDF + Logistic Regression with rule fallback."""

    trained: bool = False
    labels: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.pipeline: Pipeline | None = None
        self.label_counts: Counter[str] = Counter()

    def train(self, texts: Iterable[str], labels: Iterable[str]) -> None:
        cleaned_texts = [clean_text(text) for text in texts]
        cleaned_labels = [clean_text(label).lower() for label in labels]
        pairs = [(text, label) for text, label in zip(cleaned_texts, cleaned_labels) if text and label]
        if len(pairs) < 2 or len({label for _, label in pairs}) < 2:
            return
        train_texts = [text for text, _ in pairs]
        train_labels = [label for _, label in pairs]
        self.pipeline = Pipeline(
            steps=[
                ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_features=5000)),
                ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
            ]
        )
        self.pipeline.fit(train_texts, train_labels)
        self.labels = sorted(set(train_labels))
        self.label_counts = Counter(train_labels)
        self.trained = True

    def predict(self, text: str) -> str:
        prompt = clean_text(text)
        if self.trained and self.pipeline is not None and prompt:
            return str(self.pipeline.predict([prompt])[0])
        return self.rule_based_predict(prompt)

    def predict_proba(self, text: str) -> dict[str, float]:
        """Return probability scores when available, otherwise deterministic fallback."""
        prompt = clean_text(text)
        if self.trained and self.pipeline is not None and hasattr(self.pipeline[-1], "predict_proba"):
            probabilities = self.pipeline.predict_proba([prompt])[0]
            classes = list(self.pipeline[-1].classes_)
            return {label: round(float(prob), 4) for label, prob in zip(classes, probabilities)}
        label = self.rule_based_predict(prompt)
        return {label: float(np.float64(1.0))}

    def save(self, path: str) -> None:
        """Persist the trained classifier pipeline."""
        if self.pipeline is None:
            raise ValueError("Cannot save classifier before training.")
        joblib.dump({"pipeline": self.pipeline, "labels": self.labels}, path)

    def load(self, path: str) -> None:
        """Load a persisted classifier pipeline."""
        payload = joblib.load(path)
        self.pipeline = payload["pipeline"]
        self.labels = list(payload.get("labels", []))
        self.trained = True

    @staticmethod
    def rule_based_predict(text: str) -> str:
        lowered = text.lower()
        if any(word in lowered for word in ["seo", "rank", "keyword", "search"]):
            return "seo"
        if any(word in lowered for word in ["campaign", "launch", "funnel", "marketing"]):
            return "campaign"
        if any(word in lowered for word in ["video", "reel", "youtube", "script"]):
            return "video"
        if any(word in lowered for word in ["audio", "podcast", "voice", "narration"]):
            return "audio"
        if any(word in lowered for word in ["image", "poster", "visual", "thumbnail"]):
            return "image"
        if any(word in lowered for word in ["email", "newsletter", "subject line"]):
            return "email"
        if any(word in lowered for word in ["social", "linkedin", "instagram", "tweet"]):
            return "social"
        if any(word in lowered for word in ["blog", "article", "long form"]):
            return "blog"
        return "text"
