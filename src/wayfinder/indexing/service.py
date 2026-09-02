from wayfinder.embeddings.service import EmbeddingService
from wayfinder.ingestion.chunker import TokenChunker
from wayfinder.ingestion.models import Document
from wayfinder.retrieval.vector_store import VectorStore


class IndexingService:
    def __init__(
        self,
        chunker: TokenChunker,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ) -> None:
        self.chunker = chunker
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def index(self, document: Document) -> None:
        chunks = self.chunker.chunk(document)

        embeddings = self.embedding_service.embed_many(
            [chunk.content for chunk in chunks]
        )

        self.vector_store.upsert(
            chunks=chunks,
            embeddings=embeddings,
        )

    