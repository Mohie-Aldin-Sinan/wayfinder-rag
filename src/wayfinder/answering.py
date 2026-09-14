from wayfinder.generation.service import GenerationService
from wayfinder.ingestion.models import Chunk
from wayfinder.retrieval.service import RetrievalService


class AnsweringService:
    def __init__(
        self,
        retrieval_service: RetrievalService,
        generation_service: GenerationService,
    ) -> None:
        self.retrieval_service = retrieval_service
        self.generation_service = generation_service

    def answer(self, query: str, retrieval_k: int = 5) -> str:
        answer, _ = self.answer_with_sources(query, retrieval_k)
        return answer

    def answer_with_sources(
        self,
        query: str,
        retrieval_k: int = 5,
    ) -> tuple[str, list[Chunk]]:
        chunks = self.retrieval_service.retrieve(query, top_k=retrieval_k)
        return self.generation_service.generate(query, chunks), chunks
