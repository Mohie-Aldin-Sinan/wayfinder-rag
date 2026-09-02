from wayfinder.indexing.service import IndexingService
from wayfinder.ingestion.models import Chunk, Document


class FakeChunker:
    def chunk(self, document: Document) -> list[Chunk]:
        return [
            Chunk(
                id=f"{document.id}-chunk-0",
                document_id=document.id,
                content=document.content,
                chunk_index=0,
                metadata=document.metadata.copy(),
            )
        ]


class FakeEmbeddingService:
    def embed_many(self, texts: list[str]) -> list[list[float]]:
        return [[0.1, 0.2, 0.3] for _ in texts]


class FakeVectorStore:
    def __init__(self) -> None:
        self.chunks: list[Chunk] | None = None
        self.embeddings: list[list[float]] | None = None

    def upsert(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]],
    ) -> None:
        self.chunks = chunks
        self.embeddings = embeddings


def test_indexing_service_indexes_document():
    chunker = FakeChunker()
    embedding_service = FakeEmbeddingService()
    vector_store = FakeVectorStore()

    indexing_service = IndexingService(
        chunker=chunker,
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    document = Document(
        id="doc-1",
        content="Qdrant is a vector database.",
        metadata={
            "source_type": "documentation",
        },
    )

    indexing_service.index(document)

    assert vector_store.chunks is not None
    assert vector_store.embeddings is not None

    assert len(vector_store.chunks) == 1
    assert len(vector_store.embeddings) == 1

    assert vector_store.chunks[0].content == document.content
    assert vector_store.embeddings[0] == [0.1, 0.2, 0.3]