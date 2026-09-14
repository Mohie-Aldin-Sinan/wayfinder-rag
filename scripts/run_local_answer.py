from pathlib import Path
from uuid import uuid4

from wayfinder.answering import AnsweringService
from wayfinder.embeddings.service import EmbeddingService
from wayfinder.evaluation import load_documents
from wayfinder.generation.local import LocalGenerationService
from wayfinder.indexing.service import IndexingService
from wayfinder.ingestion.chunker import TokenChunker
from wayfinder.retrieval.hybrid import HybridRetrievalService
from wayfinder.retrieval.lexical import LexicalRetriever
from wayfinder.retrieval.qdrant_store import QdrantVectorStore
from wayfinder.retrieval.reranked import RerankedRetrievalService
from wayfinder.retrieval.reranker import CrossEncoderReranker
from wayfinder.retrieval.service import RetrievalService


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    documents = load_documents(project_root / "data" / "documents")
    chunker = TokenChunker()
    chunks = [chunk for document in documents for chunk in chunker.chunk(document)]
    embedding_service = EmbeddingService()
    vector_store = QdrantVectorStore(
        collection_name=f"wayfinder_answer_{uuid4().hex}",
        vector_size=len(embedding_service.embed("dimension probe")),
    )

    try:
        indexing_service = IndexingService(
            chunker=chunker,
            embedding_service=embedding_service,
            vector_store=vector_store,
        )
        for document in documents:
            indexing_service.index(document)

        dense = RetrievalService(embedding_service, vector_store)
        hybrid = HybridRetrievalService(dense, LexicalRetriever(chunks))
        reranked = RerankedRetrievalService(
            hybrid,
            CrossEncoderReranker(),
            candidate_k=20,
        )
        answering = AnsweringService(
            retrieval_service=reranked,
            generation_service=LocalGenerationService(),
        )

        query = "What two signals does hybrid retrieval combine?"
        answer, retrieved = answering.answer_with_sources(query, retrieval_k=3)

        print(f"query={query}")
        print(f"sources={[chunk.id for chunk in retrieved]}")
        print(f"answer={answer}")
    finally:
        vector_store.client.delete_collection(vector_store.collection_name)


if __name__ == "__main__":
    main()
