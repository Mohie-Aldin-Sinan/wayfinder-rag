from unittest.mock import Mock

from wayfinder.agentic_answering import AgenticAnsweringService
from wayfinder.ingestion.models import Chunk
from wayfinder.retrieval.agentic import AgenticRetrievalResult


def test_agentic_answering_generates_from_final_retrieval():
    chunk = Chunk(id="strong", document_id="doc", content="Evidence", chunk_index=0)
    retrieval = Mock()
    retrieval.retrieve.return_value = AgenticRetrievalResult(
        query="rewritten question",
        chunks=[chunk],
        attempts=2,
        rewritten=True,
    )
    generation = Mock()
    generation.generate.return_value = "Answer"

    result = AgenticAnsweringService(retrieval, generation).answer("original question")

    assert result.answer == "Answer"
    assert result.final_query == "rewritten question"
    assert result.attempts == 2
    assert result.rewritten is True
    generation.generate.assert_called_once_with("original question", [chunk])
