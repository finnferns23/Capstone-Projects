"""Advanced data stack tests for pandas, NumPy, and sklearn layers."""
from content_assistant.data_pipeline.data_loader import dataset_profile, load_dataframe
from content_assistant.models.content_classifier import ContentClassifier
from content_assistant.evaluation.metrics import classification_metrics
from content_assistant.services.data_insight_service import DataInsightService


def test_pandas_numpy_dataset_profile():
    frame = load_dataframe("data/datasets/ecommerce_content.csv")
    profile = dataset_profile(frame)
    assert profile["rows"] > 0
    assert "label" in profile["column_names"]


def test_sklearn_classifier_training_and_probability():
    classifier = ContentClassifier()
    classifier.train(
        ["seo keyword ranking", "podcast narration voice", "email newsletter launch", "youtube video script"],
        ["seo", "audio", "email", "video"],
    )
    prediction = classifier.predict("write an seo keyword plan")
    probabilities = classifier.predict_proba("write an seo keyword plan")
    assert prediction in {"seo", "audio", "email", "video"}
    assert probabilities


def test_classification_metrics():
    metrics = classification_metrics(["seo", "email"], ["seo", "email"])
    assert metrics["accuracy"] == 1.0
    assert metrics["macro_f1"] == 1.0


def test_data_insight_service_summary():
    summary = DataInsightService().summarize_csv("data/datasets/ecommerce_content.csv")
    assert summary["rows"] > 0
