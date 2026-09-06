from unittest.mock import Mock

from wayfinder.generation.prompts import build_grounded_prompt
from wayfinder.generation.service import GenerationService
from wayfinder.ingestion.models import Chunk


def test_build_grounded_prompt_includes_query_and_source_ids():
    chunk = Chunk(
        id="chunk-1",
        document_id="doc-1",
        content="Qdrant is a vector database.",
        chunk_index=0,
    )

    prompt = build_grounded_prompt("What is Qdrant?", [chunk])

    assert "What is Qdrant?" in prompt
    assert "[Source: chunk-1]" in prompt
    assert chunk.content in prompt
    assert "only the provided context" in prompt


def test_generate_calls_responses_api_and_returns_text():
    client = Mock()
    client.responses.create.return_value.output_text = "Qdrant is a vector database."
    service = GenerationService(client=client, model="test-model")

    result = service.generate("What is Qdrant?", [])

    assert result == "Qdrant is a vector database."
    client.responses.create.assert_called_once()
    assert client.responses.create.call_args.kwargs["model"] == "test-model"
