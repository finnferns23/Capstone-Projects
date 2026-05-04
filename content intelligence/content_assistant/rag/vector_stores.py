from pathlib import Path
from typing import List
from content_assistant.config import settings


class LocalVectorStore:
    def __init__(self) -> None:
        self.documents: list[str] = []

    def add_documents(self, documents: List[str]) -> None:
        self.documents.extend(documents)

    def similarity_search(self, query: str, limit: int = 4) -> List[str]:
        terms = set(query.lower().split())
        ranked = []
        for document in self.documents:
            score = len(terms.intersection(document.lower().split()))
            ranked.append((score, document))
        return [doc for score, doc in sorted(ranked, reverse=True) if score > 0][:limit]


class ChromaVectorStore(LocalVectorStore):
    def __init__(self, persist_dir: Path | None = None) -> None:
        super().__init__()
        self.persist_dir = persist_dir or settings.chroma_persist_dir


class PineconeVectorStore(LocalVectorStore):
    def __init__(self, index_name: str | None = None) -> None:
        super().__init__()
        self.index_name = index_name or settings.pinecone_index_name
        self.enabled = bool(settings.pinecone_api_key)
