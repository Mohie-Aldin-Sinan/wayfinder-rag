from unittest.mock import Mock

from wayfinder.evaluation.judge import LocalAnswerJudge
from wayfinder.ingestion.models import Chunk
import pytest


def test_local_answer_judge_parses_structured_scores():
    generator = Mock(return_value=[{
        "generated_text": '{"faithfulness": 1, "relevance": 0.8, "citation_quality": 1, "conciseness": 0.9, "reason": "Supported."}'
    }])
    judge = LocalAnswerJudge(generator)

    result = judge.judge(
        "What is Qdrant?",
        "Qdrant is a vector database. [Source: chunk-1]",
        [Chunk(id="chunk-1", document_id="doc-1", content="Qdrant is a vector database.", chunk_index=0)],
    )

    assert result["faithfulness"] == 1
    assert result["relevance"] == 0.8
    assert generator.call_args.kwargs["generation_config"].max_new_tokens == 128


def test_local_answer_judge_rejects_malformed_output_without_syntax_error():
    generator = Mock(return_value=[{"generated_text": "{'faithfulness': 1, broken}"}])
    judge = LocalAnswerJudge(generator)

    with pytest.raises(ValueError, match="malformed"):
        judge.judge("What is Qdrant?", "It stores vectors.", [])
