from unittest.mock import Mock

from wayfinder.answering import AnsweringService
from wayfinder.generation.service import GenerationService
from wayfinder.ingestion.models import Chunk
from wayfinder.retrieval.service import RetrievalService


def test_answer_retrieves_chunks_then_generates_from_them():
    retrieval_service = Mock(spec=RetrievalService)
    generation_service = Mock(spec=GenerationService)
    chunks = [
        Chunk(
            id="chunk-1",
            document_id="doc-1",
            content="Qdrant is a vector database.",
            chunk_index=0,
        )
    ]
    retrieval_service.retrieve.return_value = chunks
    generation_service.generate.return_value = "Qdrant is a vector database."

    service = AnsweringService(retrieval_service, generation_service)

    result = service.answer("What is Qdrant?", retrieval_k=3)

    assert result == "Qdrant is a vector database."
    retrieval_service.retrieve.assert_called_once_with(
        "What is Qdrant?", top_k=3
    )
    generation_service.generate.assert_called_once_with(
        "What is Qdrant?", chunks
    )
