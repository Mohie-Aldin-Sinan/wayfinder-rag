from unittest.mock import Mock

from wayfinder.generation.local import LocalGenerationService
from wayfinder.generation.prompts import build_grounded_prompt
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
    assert generator.call_args.kwargs["generation_config"].max_new_tokens == 128
    assert generator.call_args.kwargs["generation_config"].do_sample is False


def test_grounded_prompt_removes_documentation_promotion_but_keeps_evidence():
    chunk = Chunk(
        id="langfuse-30-chunk-1",
        document_id="langfuse-30",
        content="Want to see it in action?\nCreate a free account\nTracing records request inputs and outputs.",
        chunk_index=1,
    )

    prompt = build_grounded_prompt("What is tracing?", [chunk])

    assert "Create a free account" not in prompt
    assert "Tracing records request inputs and outputs." in prompt




def test_local_generation_refuses_without_context():
    generator = Mock()

    result = LocalGenerationService(generator=generator).generate(
        "What is the capital of France?",
        [],
    )

    assert result == "I don't have enough information in the retrieved context to answer."
    generator.assert_not_called()
