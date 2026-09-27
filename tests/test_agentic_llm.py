from unittest.mock import Mock, patch

from wayfinder.ingestion.models import Chunk
from wayfinder.retrieval.agentic_llm import HybridSufficiencyChecker, OpenRouterContextChecker, OpenRouterQueryRewriter


def test_context_checker_parses_sufficiency():
    client = Mock()
    client.chat.completions.create.return_value.choices = [
        Mock(message=Mock(content='{"sufficient": true, "reason": "Supported."}'))
    ]
    with patch("wayfinder.retrieval.agentic_llm._read_api_key", return_value="key"), patch(
        "wayfinder.retrieval.agentic_llm.OpenAI", return_value=client
    ):
        checker = OpenRouterContextChecker()
        assert checker("What is Qdrant?", [Chunk(id="c", document_id="d", content="Qdrant is a vector database.", chunk_index=0)]) is True


def test_query_rewriter_returns_rewritten_query():
    client = Mock()
    client.chat.completions.create.return_value.choices = [
        Mock(message=Mock(content='{"rewritten_query": "Qdrant vector database use cases"}'))
    ]
    with patch("wayfinder.retrieval.agentic_llm._read_api_key", return_value="key"), patch(
        "wayfinder.retrieval.agentic_llm.OpenAI", return_value=client
    ):
        rewriter = OpenRouterQueryRewriter()
        assert rewriter("What is it used for?", []) == "Qdrant vector database use cases"


def test_hybrid_checker_rejects_insufficient_keyword_overlap():
    checker = HybridSufficiencyChecker(lambda *_: True, minimum_overlap=2)
    chunks = [Chunk(id="c", document_id="d", content="A collection stores unrelated examples.", chunk_index=0)]

    assert checker("add stable identifiers", chunks) is False


def test_query_rewriter_falls_back_when_model_returns_invalid_json():
    client = Mock()
    client.chat.completions.create.return_value.choices = [
        Mock(message=Mock(content="not json"))
    ]
    with patch("wayfinder.retrieval.agentic_llm._read_api_key", return_value="key"), patch(
        "wayfinder.retrieval.agentic_llm.OpenAI", return_value=client
    ):
        rewriter = OpenRouterQueryRewriter()
        rewritten = rewriter(
            "add records",
            [Chunk(id="c", document_id="d", content="collection documents identifiers", chunk_index=0)],
        )

    assert rewritten.startswith("add records")
    assert "collection" in rewritten
