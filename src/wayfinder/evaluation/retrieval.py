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
