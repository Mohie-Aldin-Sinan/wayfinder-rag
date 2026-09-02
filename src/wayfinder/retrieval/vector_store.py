from abc import ABC, abstractmethod

from wayfinder.ingestion.models import Chunk


class VectorStore(ABC):

    @abstractmethod
    def upsert(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]],
    ) -> None:
        pass

    @abstractmethod
    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[Chunk]:
        pass