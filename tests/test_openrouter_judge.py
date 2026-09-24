from unittest.mock import Mock, patch

from wayfinder.evaluation.openrouter_judge import OpenRouterAnswerJudge


def test_openrouter_judge_uses_json_response_and_configured_model():
    response = Mock()
    response.model = "example/model:free"
    response.choices = [Mock(message=Mock(content='{"faithfulness": 1, "relevance": 1, "citation_quality": 1, "conciseness": 1, "reason": "Supported."}'))]
    with patch("wayfinder.evaluation.openrouter_judge._read_api_key", return_value="test-key"), patch(
        "wayfinder.evaluation.openrouter_judge.OpenAI"
    ) as client_class:
        client_class.return_value.chat.completions.create.return_value = response
        judge = OpenRouterAnswerJudge(model="example/model:free")
        result = judge.judge("What is Qdrant?", "A vector database.", [])

    assert result["faithfulness"] == 1
    assert result["model"] == "example/model:free"
    request = client_class.return_value.chat.completions.create.call_args.kwargs
    assert request["model"] == "example/model:free"
    assert request["response_format"] == {"type": "json_object"}
