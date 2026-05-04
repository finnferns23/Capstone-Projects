"""Capstone layer smoke tests."""
from content_assistant.data_pipeline.data_loader import load_dataset
from content_assistant.models.content_classifier import ContentClassifier
from content_assistant.services.content_optimizer import ContentOptimizer


def test_dataset_loader_reads_sample_dataset():
    rows = load_dataset("data/datasets/ecommerce_content.csv")
    assert rows
    assert {"label", "text"}.issubset(rows[0].keys())


def test_classifier_rule_based_fallback_predicts_category():
    classifier = ContentClassifier()
    assert classifier.predict("Create an SEO keyword plan") == "seo"


def test_optimizer_returns_quality_metadata():
    optimizer = ContentOptimizer()
    content, metadata = optimizer.optimize("CTA: Create value for the audience. " * 10, "campaign", "founders", "professional")
    assert "Optimization Notes" in content
    assert metadata["quality_score"] > 0
