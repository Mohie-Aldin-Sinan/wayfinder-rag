from typing import Any

from sentence_transformers import CrossEncoder

from wayfinder.ingestion.models import Chunk


class CrossEncoderReranker:
    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
        model: Any | None = None,
    ) -> None:
        self.model = model or CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        chunks: list[Chunk],
        top_k: int = 5,
    ) -> list[Chunk]:
        pairs = [(query, chunk.content) for chunk in chunks]
        scores = self.model.predict(pairs)
        ranked = sorted(
            zip(scores, chunks),
            key=lambda item: (-float(item[0]), item[1].id),
        )
        return [chunk for _, chunk in ranked[:top_k]]
