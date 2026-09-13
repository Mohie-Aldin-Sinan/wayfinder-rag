from wayfinder.ingestion.models import Chunk
from wayfinder.retrieval.reranker import CrossEncoderReranker
from wayfinder.retrieval.hybrid import HybridRetrievalService


class RerankedRetrievalService:
    def __init__(
        self,
        candidate_retrieval: HybridRetrievalService,
        reranker: CrossEncoderReranker,
        candidate_k: int = 20,
    ) -> None:
        if candidate_k <= 0:
            raise ValueError("candidate_k must be greater than zero")

        self.candidate_retrieval = candidate_retrieval
        self.reranker = reranker
        self.candidate_k = candidate_k

    def retrieve(self, query: str, top_k: int = 5) -> list[Chunk]:
        candidates = self.candidate_retrieval.retrieve(
            query,
            top_k=self.candidate_k,
        )
        return self.reranker.rerank(query, candidates, top_k=top_k)
