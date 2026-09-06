from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalEvaluationCase:
    question: str
    relevant_chunk_ids: frozenset[str]
