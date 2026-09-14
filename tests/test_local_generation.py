from unittest.mock import Mock

from wayfinder.generation.local import LocalGenerationService
from wayfinder.ingestion.models import Chunk


def test_local_generation_returns_generated_text():
    generator = Mock()
    generator.return_value = [{"generated_text": "Qdrant is a vector database."}]

    service = LocalGenerationService(generator=generator)

    chunk = Chunk(
        id="chunk-1",
        document_id="doc-1",
        content="Qdrant is a vector database.",
        chunk_index=0,
    )
    result = service.generate("What is Qdrant?", [chunk])

    assert result == (
        "Qdrant is a vector database.\n\n"
        "Sources: [Source: chunk-1]"
    )
    generator.assert_called_once()
    assert generator.call_args.args[0][0]["role"] == "system"
    assert generator.call_args.kwargs["max_new_tokens"] == 128


def test_local_generation_refuses_without_context():
    generator = Mock()

    result = LocalGenerationService(generator=generator).generate(
        "What is the capital of France?",
        [],
    )

    assert result == "I don't have enough information in the retrieved context to answer."
    generator.assert_not_called()
