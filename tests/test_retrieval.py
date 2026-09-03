from unittest.mock import Mock

from wayfinder.embeddings.service import EmbeddingService
from wayfinder.ingestion.models import Chunk
from wayfinder.retrieval.service import RetrievalService
from wayfinder.retrieval.vector_store import VectorStore


def test_retrieve_embeds_query_and_searches_vector_store():
    embedding_service = Mock(spec=EmbeddingService)
    vector_store = Mock(spec=VectorStore)

    query = "What is Qdrant?"
    query_embedding = [0.1, 0.2, 0.3]

    expected_chunks = [
        Chunk(
            id="chunk-1",
            document_id="doc-1",
            content="Qdrant is a vector database.",
            chunk_index=0,
        )
    ]

    embedding_service.embed.return_value = query_embedding
    vector_store.search.return_value = expected_chunks

    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    results = retrieval_service.retrieve(
        query=query,
        top_k=3,
    )

    embedding_service.embed.assert_called_once_with(query)

    vector_store.search.assert_called_once_with(
        query_embedding=query_embedding,
        top_k=3,
    )

    assert results == expected_chunks