from unittest.mock import Mock

from wayfinder.ingestion.models import Chunk
from wayfinder.retrieval.reranker import CrossEncoderReranker


def test_reranker_sorts_candidates_by_cross_encoder_score():
    model = Mock()
    model.predict.return_value = [0.2, 0.9]
    chunks = [
        Chunk(id="low", document_id="doc", content="Low", chunk_index=0),
        Chunk(id="high", document_id="doc", content="High", chunk_index=1),
    ]

    results = CrossEncoderReranker(model=model).rerank(
        "query",
        chunks,
        top_k=1,
    )

    assert [chunk.id for chunk in results] == ["high"]
    model.predict.assert_called_once_with([
        ("query", "Low"),
        ("query", "High"),
    ])
