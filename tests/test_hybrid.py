from unittest.mock import Mock

from wayfinder.ingestion.models import Chunk
from wayfinder.retrieval.hybrid import HybridRetrievalService
from wayfinder.retrieval.lexical import LexicalRetriever
from wayfinder.retrieval.service import RetrievalService


def test_hybrid_retrieval_rewards_chunks_present_in_both_rankings():
    shared = Chunk(
        id="shared",
        document_id="doc",
        content="Shared evidence.",
        chunk_index=0,
    )
    dense_only = Chunk(
        id="dense-only",
        document_id="doc",
        content="Dense evidence.",
        chunk_index=1,
    )
    lexical_only = Chunk(
        id="lexical-only",
        document_id="doc",
        content="Lexical evidence.",
        chunk_index=2,
    )
    dense = Mock(spec=RetrievalService)
    dense.retrieve.return_value = [shared, dense_only]
    lexical = Mock(spec=LexicalRetriever)
    lexical.search.return_value = [shared, lexical_only]

    results = HybridRetrievalService(dense, lexical).retrieve("query", top_k=3)

    assert [chunk.id for chunk in results] == ["shared", "dense-only", "lexical-only"]
