from uuid import NAMESPACE_URL, uuid5

from qdrant_client import QdrantClient, models

from wayfinder.ingestion.models import Chunk
from wayfinder.retrieval.vector_store import VectorStore


class QdrantVectorStore(VectorStore):
    def __init__(
        self,
        collection_name: str,
        vector_size: int,
        host: str = "localhost",
        port: int = 6333,
    ):
        self.collection_name = collection_name

        self.client = QdrantClient(
            host=host,
            port=port,
        )

        self._ensure_collection(vector_size)

    def _ensure_collection(self, vector_size: int) -> None:
        collections = self.client.get_collections().collections

        if any(
            collection.name == self.collection_name
            for collection in collections
        ):
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE,
            ),
        )

    def upsert(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]],
    ) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks must match number of embeddings"
            )

        points = [
            models.PointStruct(
                id=str(
                    uuid5(
                        NAMESPACE_URL,
                        chunk.id,
                    )
                ),
                vector=embedding,
                payload={
                    "chunk_id": chunk.id,
                    "content": chunk.content,
                    "document_id": chunk.document_id,
                    "chunk_index": chunk.chunk_index,
                    "metadata": chunk.metadata,
                },
            )
            for chunk, embedding in zip(chunks, embeddings)
        ]

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[Chunk]:
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=top_k,
        ).points

        return [
            Chunk(
                id=point.payload["chunk_id"],
                document_id=point.payload["document_id"],
                content=point.payload["content"],
                chunk_index=point.payload["chunk_index"],
                metadata=point.payload.get("metadata", {}),
            )
            for point in results
        ]