import json
import os
from pathlib import Path

from openai import OpenAI

from wayfinder.evaluation.judge import JUDGE_FIELDS
from wayfinder.generation.prompts import clean_context
from wayfinder.ingestion.models import Chunk


def _read_api_key() -> str:
    if os.getenv("OPENROUTER_API_KEY"):
        return os.environ["OPENROUTER_API_KEY"]
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            key, separator, value = line.partition("=")
            if separator and key.strip() == "OPENROUTER_API_KEY":
                return value.strip().strip('"').strip("'")
    raise RuntimeError("OPENROUTER_API_KEY is not configured")


class OpenRouterAnswerJudge:
    def __init__(self, model: str = "openrouter/free") -> None:
        self.model = model
        self.client = OpenAI(
            api_key=_read_api_key(),
            base_url="https://openrouter.ai/api/v1",
        )

    def judge(self, question: str, answer: str, chunks: list[Chunk]) -> dict[str, object]:
        context = "\n\n".join(
            f"[Source: {chunk.id}]\n{clean_context(chunk.content)}" for chunk in chunks
        )
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Evaluate the RAG answer using only the context. "
                        "Return JSON with numeric 0-1 scores for faithfulness, relevance, "
                        "citation_quality, conciseness, plus a short reason."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Question: {question}\n\nAnswer: {answer}\n\nContext:\n{context}",
                },
            ],
        )
        content = response.choices[0].message.content or ""
        scores = json.loads(content)
        if not JUDGE_FIELDS.issubset(scores):
            raise ValueError("OpenRouter judge JSON is missing required fields")
        scores["model"] = getattr(response, "model", self.model)
        return scores
