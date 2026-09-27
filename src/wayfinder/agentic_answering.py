from dataclasses import dataclass

from wayfinder.generation.service import GenerationService
from wayfinder.ingestion.models import Chunk
from wayfinder.retrieval.agentic import AgenticRetrievalService


@dataclass(frozen=True)
class AgenticAnswer:
    answer: str
    chunks: list[Chunk]
    final_query: str
    attempts: int
    rewritten: bool


class AgenticAnsweringService:
    def __init__(
        self,
        retrieval_service: AgenticRetrievalService,
        generation_service: GenerationService,
    ) -> None:
        self.retrieval_service = retrieval_service
        self.generation_service = generation_service

    def answer(self, query: str, retrieval_k: int = 5) -> AgenticAnswer:
        retrieval = self.retrieval_service.retrieve(query, top_k=retrieval_k)
        answer = self.generation_service.generate(query, retrieval.chunks)
        return AgenticAnswer(
            answer=answer,
            chunks=retrieval.chunks,
            final_query=retrieval.query,
            attempts=retrieval.attempts,
            rewritten=retrieval.rewritten,
        )
