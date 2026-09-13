from wayfinder.ingestion.models import Chunk
from wayfinder.retrieval.lexical import LexicalRetriever
from wayfinder.retrieval.service import RetrievalService


class HybridRetrievalService:
    def __init__(
        self,
        dense_retrieval: RetrievalService,
        lexical_retrieval: LexicalRetriever,
        rank_constant: int = 60,
    ) -> None:
        self.dense_retrieval = dense_retrieval
        self.lexical_retrieval = lexical_retrieval
        self.rank_constant = rank_constant

    def retrieve(self, query: str, top_k: int = 5) -> list[Chunk]:
        dense_chunks = self.dense_retrieval.retrieve(query, top_k=top_k)
        lexical_chunks = self.lexical_retrieval.search(query, top_k=top_k)
        scores: dict[str, float] = {}
        chunks_by_id: dict[str, Chunk] = {}

        for ranked_chunks in (dense_chunks, lexical_chunks):
            for rank, chunk in enumerate(ranked_chunks, start=1):
                chunks_by_id[chunk.id] = chunk
                scores[chunk.id] = scores.get(chunk.id, 0.0) + (
                    1 / (self.rank_constant + rank)
                )

        ranked_ids = sorted(
            scores,
            key=lambda chunk_id: (-scores[chunk_id], chunk_id),
        )
        return [chunks_by_id[chunk_id] for chunk_id in ranked_ids[:top_k]]
