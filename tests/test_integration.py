from uuid import uuid4

from wayfinder.embeddings.service import EmbeddingService
from wayfinder.indexing.service import IndexingService
from wayfinder.ingestion.chunker import TokenChunker
from wayfinder.ingestion.models import Document
from wayfinder.retrieval.qdrant_store import QdrantVectorStore


def test_document_is_indexed_and_retrievable_from_qdrant():
    collection_name = f"wayfinder_test_{uuid4().hex}"

    vector_store = QdrantVectorStore(
        collection_name=collection_name,
        vector_size=1024,
    )

    try:
        document = Document(
            id="integration-doc-1",
            content=(
                "Qdrant is a vector database designed for similarity search. "
                "It stores vector embeddings and retrieves semantically similar data."
            ),
            metadata={
                "source": "integration-test",
            },
        )

        chunker = TokenChunker(
            chunk_size=50,
            overlap=10,
        )

        embedding_service = EmbeddingService()

        indexing_service = IndexingService(
            chunker=chunker,
            embedding_service=embedding_service,
            vector_store=vector_store,
        )

        indexing_service.index(document)

        query_embedding = embedding_service.embed(
            "What is Qdrant?"
        )

        results = vector_store.client.query_points(
            collection_name=collection_name,
            query=query_embedding,
            limit=5,
        ).points

        assert len(results) > 0
        assert results[0].payload["document_id"] == document.id

    finally:
        vector_store.client.delete_collection(
            collection_name=collection_name,
        )