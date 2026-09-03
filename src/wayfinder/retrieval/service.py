from wayfinder.embeddings.service import EmbeddingService
from wayfinder.ingestion.models import Chunk
from wayfinder.retrieval.vector_store import VectorStore


class RetrievalService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ) -> None:
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[Chunk]:
        query_embedding = self.embedding_service.embed(query)

        return self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )