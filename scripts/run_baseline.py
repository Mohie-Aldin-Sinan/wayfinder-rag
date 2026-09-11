from pathlib import Path
from uuid import uuid4

from wayfinder.embeddings.service import EmbeddingService
from wayfinder.evaluation import (
    evaluate_retrieval,
    load_documents,
    load_evaluation_cases,
)
from wayfinder.indexing.service import IndexingService
from wayfinder.ingestion.chunker import TokenChunker
from wayfinder.retrieval.qdrant_store import QdrantVectorStore
from wayfinder.retrieval.service import RetrievalService


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    documents = load_documents(project_root / "data" / "documents")
    cases = load_evaluation_cases(project_root / "data" / "evaluation_cases.json")

    embedding_service = EmbeddingService()
    vector_store = QdrantVectorStore(
        collection_name=f"wayfinder_baseline_{uuid4().hex}",
        vector_size=len(embedding_service.embed("dimension probe")),
    )

    try:
        indexing_service = IndexingService(
            chunker=TokenChunker(),
            embedding_service=embedding_service,
            vector_store=vector_store,
        )

        for document in documents:
            indexing_service.index(document)

        score = evaluate_retrieval(
            RetrievalService(embedding_service, vector_store),
            cases,
            top_k=5,
        )
        print(f"dense_retrieval_recall_at_5={score:.3f}")
    finally:
        vector_store.client.delete_collection(vector_store.collection_name)


if __name__ == "__main__":
    main()
