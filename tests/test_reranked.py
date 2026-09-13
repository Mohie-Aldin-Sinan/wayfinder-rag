from unittest.mock import Mock

from wayfinder.ingestion.models import Chunk
from wayfinder.retrieval.hybrid import HybridRetrievalService
from wayfinder.retrieval.reranked import RerankedRetrievalService
from wayfinder.retrieval.reranker import CrossEncoderReranker


def test_reranked_retrieval_uses_broad_candidates_then_final_top_k():
    candidates = [
        Chunk(id="one", document_id="doc", content="One", chunk_index=0),
        Chunk(id="two", document_id="doc", content="Two", chunk_index=1),
    ]
    candidate_retrieval = Mock(spec=HybridRetrievalService)
    candidate_retrieval.retrieve.return_value = candidates
    reranker = Mock(spec=CrossEncoderReranker)
    reranker.rerank.return_value = [candidates[1]]

    service = RerankedRetrievalService(candidate_retrieval, reranker, candidate_k=10)

    assert service.retrieve("query", top_k=1) == [candidates[1]]
    candidate_retrieval.retrieve.assert_called_once_with("query", top_k=10)
    reranker.rerank.assert_called_once_with("query", candidates, top_k=1)
