# AI Content Intelligence Capstone

A production-ready, multi-modular, multimedia AI assistant for planning, generating, repurposing, and exporting content across text, blogs, email, social posts, SEO, audio scripts, video scripts, image prompts, and full campaigns.

## Core Capabilities

- Multi-agent content generation with separate Python files for each agent
- Async orchestration through a central assistant workflow
- LangChain and LangGraph ready architecture
- OpenAI integration with safe local fallback when API keys are missing
- Hybrid memory using JSON memory and vector memory
- RAG support through a local knowledge base
- Chroma and Pinecone ready vector store layer
- ElevenLabs ready voice generation layer
- CLI and Streamlit entry points
- Logging, error handling, and export services included

## Architecture

```text
User Input
  -> Validation Service
  -> Safety Guard
  -> Memory Recall
  -> RAG Retriever
  -> Router
  -> Specialized Agent
  -> Export Service
  -> Memory Save
  -> Final Response
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Add your keys later in `.env`:

```env
OPENAI_API_KEY=
PINECONE_API_KEY=
ELEVENLABS_API_KEY=
```

The project runs without keys using local fallback mode.

## Run CLI

```bash
python main.py --task campaign --prompt "Create a launch campaign for an AI productivity assistant"
```

## Run Streamlit

```bash
streamlit run app.py
```

## Run Validation

```bash
python -m compileall .
python -m pytest tests
python main.py --task text --prompt "Create a short content plan"
```

## Production Notes

- No API keys are hardcoded
- Missing external API keys do not crash local execution
- Logs are handled through `content_assistant/utils/logging_config.py`
- Outputs are exported into the `outputs/` folder
- Memory is stored in `data/assistant_memory.json`
- Knowledge files can be added to `data/knowledge_base/`

## Folder Structure

```text
content_assistant/
  agents/       Specialized content agents
  core/         Routing, safety, formatting
  graph/        Workflow description and LangGraph-ready layer
  memory/       JSON and vector memory
  rag/          Retriever and vector store abstractions
  schemas/      Request and response schemas
  services/     LLM, memory, RAG, export, validation services
  tools/        Reusable content utilities
  utils/        Logging and helpers
  voice/        ElevenLabs and voice interface
  workers/      Async runner utilities
```


## Capstone-Level Additions

This final version upgrades the assistant from a content generator into an AI content intelligence platform:

- Dataset layer with Kaggle-style sample CSV files under `data/datasets/`
- Data pipeline for loading and cleaning content datasets
- Lightweight ML classifier for content category prediction
- Rule-based fallback when ML libraries are unavailable
- Evaluation helpers for accuracy, label distribution, and output quality scoring
- Content optimization layer that adds quality notes and improvement guidance
- Usage analytics stored as JSONL in the outputs folder
- Capstone report under `docs/CAPSTONE_REPORT.md`

### Recommended Kaggle Dataset Extensions

The project is ready to accept public text/content datasets such as ecommerce text classification, news article classification, product title classification, and multimodal ecommerce datasets. Add downloaded CSV files into `data/datasets/`, keeping columns named `label` and `text` for immediate compatibility.

### Capstone Validation Commands

```bash
python main.py --task campaign --prompt "Create a launch campaign for an AI content platform"
pytest
```


## Optional ML Upgrade

The bundled capstone classifier is intentionally lightweight and reliable. If you want to experiment with larger Kaggle datasets, you can optionally add pandas, numpy, and scikit-learn later for notebook-based model comparison. The production app does not require them to run.

## Advanced Data Science Stack Upgrade

This capstone version includes a real data-science layer instead of only prompt routing.

Added production-capstone packages and modules:

- pandas and NumPy for dataset loading, cleaning, profiling, and analytics.
- scikit-learn and SciPy for TF-IDF feature extraction and Logistic Regression classification.
- joblib for optional model persistence.
- Chroma and Pinecone for local and cloud vector memory readiness.
- LangChain and LangGraph for orchestration-ready AI workflows.
- OpenAI and ElevenLabs integrations with safe fallback when keys are missing.
- FastAPI and Uvicorn as optional deployment-ready backend packages.
- Rich, tqdm, requests, aiofiles, and PyYAML as supporting production utilities.

### Capstone ML Flow

```text
CSV datasets -> pandas cleaning -> TF-IDF features -> Logistic Regression classifier -> category routing -> RAG -> content agents -> optimization -> analytics tracking
```

### New Advanced Modules

```text
content_assistant/data_pipeline/data_loader.py       # pandas CSV loading and profiling
content_assistant/data_pipeline/data_cleaner.py      # pandas and NumPy cleaning helpers
content_assistant/models/content_classifier.py       # sklearn TF-IDF classifier
content_assistant/evaluation/metrics.py              # accuracy, precision, recall, F1, quality score
content_assistant/services/data_insight_service.py   # dataset insight summaries
content_assistant/analytics/usage_tracker.py         # JSONL tracking with pandas summaries
```


## Capstone Positioning

This project is built for a capstone project category. It combines:

- Dataset-driven content classification with pandas, NumPy, and scikit-learn.
- Multi-agent content generation across text, blog, social, email, audio, video, image prompts, campaign planning, SEO, and repurposing.
- RAG-style context retrieval from the local knowledge base.
- Hybrid memory with JSON persistence and vector-memory adapters for Chroma and Pinecone readiness.
- Async orchestration with production-safe fallback behavior when API keys are not configured.
- Grounding metadata so generated outputs can expose whether local knowledge and sample datasets were used.

## Kaggle Dataset Readiness

The project includes small representative CSV samples to keep the repository lightweight and runnable. For full capstone experimentation, download compatible Kaggle datasets manually and place them in `data/datasets/`. Recommended sources are documented in `docs/KAGGLE_DATA_REFERENCES.md`.

## Final Validation Commands

```bash
python -m compileall -q .
python main.py
python -m pytest -q
```

After installing requirements, the Streamlit UI can be launched with:

```bash
streamlit run app.py
```

## Kaggle Dataset Support

This capstone includes a Kaggle support layer for dataset driven content intelligence workflows. The files under `data/kaggle_configs/`, `scripts/`, `content_assistant/data_pipeline/`, and `content_assistant/services/kaggle_ingestion_service.py` help map external Kaggle CSV datasets into the project pipeline without changing the core assistant logic.

Recommended placement is already completed in this final package:

```text
data/kaggle_configs/                         # dataset registry JSON
scripts/download_kaggle_datasets.py          # optional Kaggle download helper
scripts/ingest_kaggle_assets.py              # ingestion helper
content_assistant/data_pipeline/             # schema registry and mapping
content_assistant/services/                  # Kaggle ingestion service
tests/test_kaggle_addon.py                   # validation test
```

To use real Kaggle downloads later, configure your Kaggle credentials locally and run:

```bash
python scripts/download_kaggle_datasets.py
python scripts/ingest_kaggle_assets.py
```

The project still runs without Kaggle credentials because sample capstone datasets are included locally.
