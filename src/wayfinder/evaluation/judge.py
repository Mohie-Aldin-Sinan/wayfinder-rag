import json
import ast
import re
from typing import Any

from transformers import GenerationConfig

from wayfinder.generation.prompts import clean_context
from wayfinder.ingestion.models import Chunk


JUDGE_FIELDS = {"faithfulness", "relevance", "citation_quality", "conciseness", "reason"}


class LocalAnswerJudge:
    def __init__(self, generator: Any, max_new_tokens: int = 128) -> None:
        self.generator = generator
        self.generation_config = GenerationConfig(
            max_new_tokens=max_new_tokens,
            do_sample=False,
        )

    def judge(self, question: str, answer: str, chunks: list[Chunk]) -> dict[str, Any]:
        context = "\n\n".join(
            f"[Source: {chunk.id}]\n{clean_context(chunk.content)}"
            for chunk in chunks
        )
        prompt = (
            "You are evaluating a RAG answer. Score each category from 0 to 1. "
            "Return only valid JSON with numeric keys faithfulness, relevance, "
            "citation_quality, conciseness, and a short reason.\n\n"
            f"Question: {question}\n\nAnswer: {answer}\n\nContext:\n{context}"
        )
        result = self.generator(prompt, generation_config=self.generation_config)
        text = result[0]["generated_text"] if isinstance(result, list) else result["generated_text"]
        match = re.search(r"\{[^{}]*\}", text, re.DOTALL)
        if not match:
            raise ValueError("Judge did not return a JSON object")
        raw_scores = match.group(0)
        try:
            scores = json.loads(raw_scores)
        except json.JSONDecodeError:
            try:
                scores = ast.literal_eval(raw_scores)
            except (SyntaxError, ValueError) as error:
                raise ValueError("Judge returned malformed structured output") from error
        if not JUDGE_FIELDS.issubset(scores):
            raise ValueError("Judge JSON is missing required fields")
        return scores
