from collections.abc import Sequence

from wayfinder.evaluation.models import RetrievalEvaluationCase
from wayfinder.ingestion.models import Chunk
from wayfinder.retrieval.service import RetrievalService


def recall_at_k(
    evaluation_case: RetrievalEvaluationCase,
    retrieved_chunks: Sequence[Chunk],
) -> float:
    retrieved_ids = {chunk.id for chunk in retrieved_chunks}

    if not evaluation_case.relevant_chunk_ids:
        raise ValueError("Evaluation case must contain relevant chunk IDs")

    relevant_ids_retrieved = retrieved_ids & evaluation_case.relevant_chunk_ids
    return len(relevant_ids_retrieved) / len(evaluation_case.relevant_chunk_ids)


def reciprocal_rank(
    evaluation_case: RetrievalEvaluationCase,
    retrieved_chunks: Sequence[Chunk],
) -> float:
    for rank, chunk in enumerate(retrieved_chunks, start=1):
        if chunk.id in evaluation_case.relevant_chunk_ids:
            return 1.0 / rank

    return 0.0


def hit_at_k(
    evaluation_case: RetrievalEvaluationCase,
    retrieved_chunks: Sequence[Chunk],
    k: int,
) -> float:
    if k <= 0:
        raise ValueError("k must be greater than zero")

    return float(
        any(
            chunk.id in evaluation_case.relevant_chunk_ids
            for chunk in retrieved_chunks[:k]
        )
    )


def document_recall_at_k(
    evaluation_case: RetrievalEvaluationCase,
    retrieved_chunks: Sequence[Chunk],
) -> float:
    """Measure recall after collapsing chunk IDs to parent document IDs."""
    relevant_documents = {
        chunk_id.split("-chunk-", maxsplit=1)[0]
        for chunk_id in evaluation_case.relevant_chunk_ids
    }
    retrieved_documents = {chunk.document_id for chunk in retrieved_chunks}
    return len(relevant_documents & retrieved_documents) / len(relevant_documents)


def document_hit_at_k(
    evaluation_case: RetrievalEvaluationCase,
    retrieved_chunks: Sequence[Chunk],
    k: int,
) -> float:
    if k <= 0:
        raise ValueError("k must be greater than zero")
    relevant_documents = {
        chunk_id.split("-chunk-", maxsplit=1)[0]
        for chunk_id in evaluation_case.relevant_chunk_ids
    }
    return float(any(chunk.document_id in relevant_documents for chunk in retrieved_chunks[:k]))


def evaluate_retrieval(
    retrieval_service: RetrievalService,
    evaluation_cases: Sequence[RetrievalEvaluationCase],
    top_k: int = 5,
) -> float:
    if not evaluation_cases:
        raise ValueError("Evaluation dataset must contain at least one case")

    scores = [
        recall_at_k(
            evaluation_case,
            retrieval_service.retrieve(evaluation_case.question, top_k=top_k),
        )
        for evaluation_case in evaluation_cases
    ]

    return sum(scores) / len(scores)
