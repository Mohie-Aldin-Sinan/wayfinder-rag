from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from wayfinder.ingestion.models import Chunk


SufficiencyChecker = Callable[[str, list[Chunk]], bool]
QueryRewriter = Callable[[str, list[Chunk]], str]


@dataclass(frozen=True)
class AgenticRetrievalResult:
    query: str
    chunks: list[Chunk]
    attempts: int
    rewritten: bool


class AgenticRetrievalService:
    """Run a bounded retrieve-check-rewrite-retrieve loop."""

    def __init__(
        self,
        retrieval_service,
        sufficiency_checker: SufficiencyChecker,
        query_rewriter: QueryRewriter,
        max_attempts: int = 2,
        trace_recorder: Any | None = None,
    ) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        self.retrieval_service = retrieval_service
        self.sufficiency_checker = sufficiency_checker
        self.query_rewriter = query_rewriter
        self.max_attempts = max_attempts
        self.trace_recorder = trace_recorder

    def retrieve(self, query: str, top_k: int = 5) -> AgenticRetrievalResult:
        current_query = query
        rewritten = False

        for attempt in range(1, self.max_attempts + 1):
            if self.trace_recorder:
                self.trace_recorder.record(
                    "agentic_retrieval_attempt",
                    attempt=attempt,
                    query=current_query,
                )
            chunks = self.retrieval_service.retrieve(current_query, top_k=top_k)
            try:
                sufficient = self.sufficiency_checker(current_query, chunks)
            except Exception as error:
                if self.trace_recorder:
                    self.trace_recorder.record(
                        "context_sufficiency_error",
                        attempt=attempt,
                        error=str(error),
                    )
                sufficient = True
            if self.trace_recorder:
                self.trace_recorder.record(
                    "context_sufficiency_checked",
                    attempt=attempt,
                    sufficient=sufficient,
                    chunk_ids=[chunk.id for chunk in chunks],
                    document_ids=[chunk.document_id for chunk in chunks],
                    projects=[chunk.metadata.get("project") for chunk in chunks],
                )
            if sufficient or attempt == self.max_attempts:
                return AgenticRetrievalResult(current_query, chunks, attempt, rewritten)
            try:
                current_query = self.query_rewriter(current_query, chunks)
            except Exception as error:
                if self.trace_recorder:
                    self.trace_recorder.record(
                        "query_rewrite_error",
                        attempt=attempt,
                        error=str(error),
                    )
                return AgenticRetrievalResult(current_query, chunks, attempt, rewritten)
            if not current_query.strip():
                raise ValueError("query_rewriter must return a non-empty query")
            rewritten = True
            if self.trace_recorder:
                self.trace_recorder.record(
                    "query_rewritten",
                    attempt=attempt,
                    rewritten_query=current_query,
                )

        raise RuntimeError("agentic retrieval loop exited unexpectedly")
