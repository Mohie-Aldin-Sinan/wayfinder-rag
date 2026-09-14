from typing import Any

from transformers import pipeline

from wayfinder.generation.prompts import (
    attach_source_citations,
    build_grounded_prompt,
)
from wayfinder.ingestion.models import Chunk


class LocalGenerationService:
    def __init__(
        self,
        model_name: str = "HuggingFaceTB/SmolLM2-360M-Instruct",
        generator: Any | None = None,
    ) -> None:
        self.generator = generator or pipeline(
            "text-generation",
            model=model_name,
        )

    def generate(self, query: str, chunks: list[Chunk]) -> str:
        if not chunks:
            return "I don't have enough information in the retrieved context to answer."

        messages = [
            {
                "role": "system",
                "content": (
                    "Answer only from the provided context. "
                    "If the context is insufficient, say so. "
                    "Ignore navigation and marketing text. "
                    "Give a concise answer in 1-3 sentences. "
                    "Cite source IDs when answering."
                ),
            },
            {
                "role": "user",
                "content": build_grounded_prompt(query, chunks),
            },
        ]
        result = self.generator(
            messages,
            max_new_tokens=128,
            do_sample=False,
        )
        generated = result[0]["generated_text"]
        if isinstance(generated, list):
            answer = generated[-1]["content"].strip()
        else:
            answer = generated.strip()

        return attach_source_citations(answer, chunks)
