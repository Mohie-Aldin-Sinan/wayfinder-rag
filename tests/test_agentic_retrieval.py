from unittest.mock import Mock

import pytest

from wayfinder.ingestion.models import Chunk
from wayfinder.retrieval.agentic import AgenticRetrievalService


def chunk(identifier: str) -> Chunk:
    return Chunk(id=identifier, document_id="doc", content="evidence", chunk_index=0)


def test_agentic_retrieval_stops_when_first_context_is_sufficient():
    retrieval = Mock()
    retrieval.retrieve.return_value = [chunk("first")]
    checker = Mock(return_value=True)
    rewriter = Mock()
    service = AgenticRetrievalService(retrieval, checker, rewriter)

    result = service.retrieve("original question")

    assert result.query == "original question"
    assert result.attempts == 1
    assert result.rewritten is False
    rewriter.assert_not_called()


def test_agentic_retrieval_rewrites_once_when_context_is_insufficient():
    retrieval = Mock()
    retrieval.retrieve.side_effect = [[chunk("weak")], [chunk("strong")]]
    checker = Mock(side_effect=[False, True])
    rewriter = Mock(return_value="more specific question")
    service = AgenticRetrievalService(retrieval, checker, rewriter)

    result = service.retrieve("original question")

    assert result.query == "more specific question"
    assert result.chunks[0].id == "strong"
    assert result.attempts == 2
    assert result.rewritten is True
    assert retrieval.retrieve.call_args_list[1].args[0] == "more specific question"


def test_agentic_retrieval_records_decisions():
    retrieval = Mock()
    retrieval.retrieve.side_effect = [[chunk("weak")], [chunk("strong")]]
    trace = Mock()
    service = AgenticRetrievalService(
        retrieval,
        Mock(side_effect=[False, True]),
        Mock(return_value="rewritten"),
        trace_recorder=trace,
    )

    service.retrieve("question")

    events = [call.args[0] for call in trace.record.call_args_list]
    assert events == [
        "agentic_retrieval_attempt",
        "context_sufficiency_checked",
        "query_rewritten",
        "agentic_retrieval_attempt",
        "context_sufficiency_checked",
    ]


def test_agentic_retrieval_rejects_empty_rewritten_query():
    retrieval = Mock()
    retrieval.retrieve.return_value = [chunk("weak")]
    service = AgenticRetrievalService(retrieval, lambda *_: False, lambda *_: "  ")

    with pytest.raises(ValueError, match="non-empty"):
        service.retrieve("question")


def test_agentic_retrieval_keeps_context_when_checker_fails():
    retrieval = Mock()
    retrieval.retrieve.return_value = [chunk("available")]
    service = AgenticRetrievalService(retrieval, Mock(side_effect=RuntimeError("rate limit")), Mock())

    result = service.retrieve("question")

    assert result.chunks[0].id == "available"
    assert result.attempts == 1
    assert result.rewritten is False
