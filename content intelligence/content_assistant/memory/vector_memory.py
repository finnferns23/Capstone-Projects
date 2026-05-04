from typing import List


class VectorMemory:
    def __init__(self) -> None:
        self.records: list[str] = []

    async def add_text(self, text: str) -> None:
        self.records.append(text)

    async def search(self, query: str, limit: int = 3) -> List[str]:
        query_terms = set(query.lower().split())
        scored = []
        for record in self.records:
            score = len(query_terms.intersection(record.lower().split()))
            scored.append((score, record))
        return [record for score, record in sorted(scored, reverse=True) if score > 0][:limit]
