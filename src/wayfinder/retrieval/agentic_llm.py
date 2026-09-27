import json
import re

from wayfinder.evaluation.openrouter_judge import _read_api_key
from wayfinder.generation.prompts import clean_context
from wayfinder.ingestion.models import Chunk
from openai import OpenAI


STOPWORDS = {"what", "where", "when", "which", "how", "does", "do", "the", "a", "an", "is", "are", "to", "of", "and", "in", "for", "my", "can", "i"}


def _meaningful_terms(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.casefold())
        if token.isalpha() and len(token) > 3 and token not in STOPWORDS
    }


class HybridSufficiencyChecker:
    def __init__(self, semantic_checker, minimum_overlap: int = 2) -> None:
        self.semantic_checker = semantic_checker
        self.minimum_overlap = minimum_overlap

    def __call__(self, query: str, chunks: list[Chunk]) -> bool:
        if not self.semantic_checker(query, chunks):
            return False
        query_terms = _meaningful_terms(query)
        context_terms = _meaningful_terms(" ".join(chunk.content for chunk in chunks))
        return len(query_terms & context_terms) >= self.minimum_overlap


class OpenRouterContextChecker:
    def __init__(self, model: str = "openrouter/free") -> None:
        self.model = model
        self.client = OpenAI(
            api_key=_read_api_key(),
            base_url="https://openrouter.ai/api/v1",
        )

    def __call__(self, query: str, chunks: list[Chunk]) -> bool:
        context = "\n\n".join(clean_context(chunk.content) for chunk in chunks)
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "Return JSON with boolean sufficient and a short reason. Mark sufficient only when the context directly supports an answer.",
                },
                {"role": "user", "content": f"Question: {query}\n\nContext:\n{context}"},
            ],
        )
        result = json.loads(response.choices[0].message.content or "{}")
        if not isinstance(result.get("sufficient"), bool):
            raise ValueError("Context checker returned invalid sufficiency")
        return result["sufficient"]


class OpenRouterQueryRewriter:
    def __init__(self, model: str = "openrouter/free") -> None:
        self.model = model
        self.client = OpenAI(
            api_key=_read_api_key(),
            base_url="https://openrouter.ai/api/v1",
        )

    def __call__(self, query: str, chunks: list[Chunk]) -> str:
        context = "\n\n".join(clean_context(chunk.content) for chunk in chunks)
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "Rewrite the question for better documentation retrieval. Return JSON with one concise rewritten_query string. Do not answer the question.",
                },
                {"role": "user", "content": f"Original question: {query}\n\nWeak context:\n{context}"},
            ],
        )
        try:
            result = json.loads(response.choices[0].message.content or "{}")
            rewritten = result.get("rewritten_query")
            if isinstance(rewritten, str) and rewritten.strip():
                return rewritten.strip()
        except json.JSONDecodeError:
            pass

        context_terms = sorted(_meaningful_terms(context), key=lambda term: (-context.casefold().count(term), term))[:8]
        fallback = " ".join([query.strip(), *context_terms]).strip()
        if not fallback:
            raise ValueError("Query rewriter returned an invalid query")
        return fallback
