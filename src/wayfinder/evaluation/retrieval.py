from collections.abc import Sequence

from wayfinder.evaluation.models import RetrievalEvaluationCase
from wayfinder.ingestion.models import Chunk


def recall_at_k(
    evaluation_case: RetrievalEvaluationCase,
    retrieved_chunks: Sequence[Chunk],
) -> float:
    retrieved_ids = {chunk.id for chunk in retrieved_chunks}

    if not evaluation_case.relevant_chunk_ids:
        raise ValueError("Evaluation case must contain relevant chunk IDs")

    relevant_ids_retrieved = retrieved_ids & evaluation_case.relevant_chunk_ids
    return len(relevant_ids_retrieved) / len(evaluation_case.relevant_chunk_ids)
