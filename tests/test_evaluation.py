import pytest

from wayfinder.evaluation import RetrievalEvaluationCase, recall_at_k
from wayfinder.ingestion.models import Chunk


def test_recall_at_k_is_one_when_a_relevant_chunk_is_retrieved():
    case = RetrievalEvaluationCase(
        question="What is Qdrant?",
        relevant_chunk_ids=frozenset({"chunk-1"}),
    )
    chunks = [
        Chunk(
            id="chunk-1",
            document_id="doc-1",
            content="Qdrant is a vector database.",
            chunk_index=0,
        )
    ]

    assert recall_at_k(case, chunks) == 1.0


def test_recall_at_k_is_zero_when_no_relevant_chunk_is_retrieved():
    case = RetrievalEvaluationCase(
        question="What is Qdrant?",
        relevant_chunk_ids=frozenset({"chunk-1"}),
    )
    chunks = [
        Chunk(
            id="chunk-2",
            document_id="doc-1",
            content="Qdrant stores vectors.",
            chunk_index=1,
        )
    ]

    assert recall_at_k(case, chunks) == 0.0


def test_recall_at_k_rejects_empty_ground_truth():
    case = RetrievalEvaluationCase(
        question="What is Qdrant?",
        relevant_chunk_ids=frozenset(),
    )

    with pytest.raises(ValueError, match="relevant chunk IDs"):
        recall_at_k(case, [])


def test_recall_at_k_measures_fraction_of_relevant_chunks_retrieved():
    case = RetrievalEvaluationCase(
        question="What is Qdrant?",
        relevant_chunk_ids=frozenset({"chunk-1", "chunk-2"}),
    )
    chunks = [
        Chunk(
            id="chunk-1",
            document_id="doc-1",
            content="Qdrant is a vector database.",
            chunk_index=0,
        )
    ]

    assert recall_at_k(case, chunks) == 0.5
