from pathlib import Path
from typing import List
from content_assistant.config import settings
from content_assistant.rag.vector_stores import ChromaVectorStore, LocalVectorStore, PineconeVectorStore


class RagRetriever:
    def __init__(self) -> None:
        self.local_store = LocalVectorStore()
        self.chroma_store = ChromaVectorStore()
        self.pinecone_store = PineconeVectorStore()
        self._load_knowledge_base(settings.knowledge_base_dir)

    def _load_knowledge_base(self, directory: Path) -> None:
        directory.mkdir(parents=True, exist_ok=True)
        documents: List[str] = []
        for path in directory.glob("*.md"):
            text = path.read_text(encoding="utf-8").strip()
            if text:
                documents.append(text)
        self.local_store.add_documents(documents)
        self.chroma_store.add_documents(documents)
        self.pinecone_store.add_documents(documents)

    async def retrieve(self, query: str) -> List[str]:
        results = self.local_store.similarity_search(query)
        if not results:
            results = self.chroma_store.similarity_search(query)
        if not results and self.pinecone_store.enabled:
            results = self.pinecone_store.similarity_search(query)
        return results
