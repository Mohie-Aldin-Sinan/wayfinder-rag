from wayfinder.generation.service import GenerationService
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
        chunks = self.retrieval_service.retrieve(query, top_k=retrieval_k)
        return self.generation_service.generate(query, chunks)
