from unittest.mock import Mock
from pathlib import Path

import pytest

from wayfinder.evaluation import (
    RetrievalEvaluationCase,
    evaluate_retrieval,
    hit_at_k,
    load_documents,
    load_evaluation_cases,
    load_source_manifest,
    recall_at_k,
    document_recall_at_k,
    reciprocal_rank,
)
from wayfinder.ingestion.models import Chunk
from wayfinder.retrieval.service import RetrievalService


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


def test_document_recall_accepts_a_different_chunk_from_the_same_document():
    case = RetrievalEvaluationCase(
        question="What is Qdrant?",
        relevant_chunk_ids=frozenset({"qdrant-0-chunk-11"}),
    )
    chunks = [Chunk(id="qdrant-0-chunk-1", document_id="qdrant-0", content="Relevant page", chunk_index=1)]

    assert document_recall_at_k(case, chunks) == 1.0


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


def test_evaluate_retrieval_returns_mean_recall():
    retrieval_service = Mock(spec=RetrievalService)
    retrieval_service.retrieve.side_effect = [
        [
            Chunk(
                id="chunk-1",
                document_id="doc-1",
                content="Relevant content.",
                chunk_index=0,
            )
        ],
        [],
    ]
    cases = [
        RetrievalEvaluationCase(
            question="Question one",
            relevant_chunk_ids=frozenset({"chunk-1"}),
        ),
        RetrievalEvaluationCase(
            question="Question two",
            relevant_chunk_ids=frozenset({"chunk-2"}),
        ),
    ]

    assert evaluate_retrieval(retrieval_service, cases, top_k=3) == 0.5
    assert retrieval_service.retrieve.call_count == 2


def test_load_documents_and_evaluation_cases(tmp_path: Path):
    documents_dir = tmp_path / "documents"
    documents_dir.mkdir()
    (documents_dir / "qdrant.md").write_text("Qdrant stores vectors.", encoding="utf-8")
    cases_path = tmp_path / "cases.json"
    cases_path.write_text(
        '[{"question": "What stores vectors?", '
        '"relevant_chunk_ids": ["qdrant-chunk-0"]}]',
        encoding="utf-8",
    )

    documents = load_documents(documents_dir)
    cases = load_evaluation_cases(cases_path)

    assert documents[0].id == "qdrant"
    assert documents[0].content == "Qdrant stores vectors."
    assert cases[0].relevant_chunk_ids == frozenset({"qdrant-chunk-0"})


def test_load_source_manifest(tmp_path: Path):
    manifest_path = tmp_path / "sources.json"
    manifest_path.write_text(
        '[{"project": "Qdrant", "source_url": "https://qdrant.tech"}]',
        encoding="utf-8",
    )

    manifest = load_source_manifest(manifest_path)

    assert manifest[0]["project"] == "Qdrant"


def test_ranking_metrics_reward_relevant_chunks_near_the_top():
    case = RetrievalEvaluationCase(
        question="What is Qdrant?",
        relevant_chunk_ids=frozenset({"chunk-2"}),
    )
    chunks = [
        Chunk(id="chunk-1", document_id="doc", content="Other", chunk_index=0),
        Chunk(id="chunk-2", document_id="doc", content="Relevant", chunk_index=1),
    ]

    assert hit_at_k(case, chunks, k=1) == 0.0
    assert hit_at_k(case, chunks, k=2) == 1.0
    assert reciprocal_rank(case, chunks) == 0.5
