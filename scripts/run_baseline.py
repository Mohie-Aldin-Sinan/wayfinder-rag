from pathlib import Path
from uuid import uuid4
import argparse

from wayfinder.embeddings.service import EmbeddingService
from wayfinder.evaluation import (
    hit_at_k,
    document_hit_at_k,
    document_recall_at_k,
    load_documents,
    load_evaluation_cases,
    recall_at_k,
    reciprocal_rank,
)
from wayfinder.indexing.service import IndexingService
from wayfinder.ingestion.chunker import TokenChunker
from wayfinder.retrieval.qdrant_store import QdrantVectorStore
from wayfinder.retrieval.hybrid import HybridRetrievalService
from wayfinder.retrieval.lexical import LexicalRetriever
from wayfinder.retrieval.reranked import RerankedRetrievalService
from wayfinder.retrieval.reranker import CrossEncoderReranker
from wayfinder.retrieval.service import RetrievalService


def report_metrics(label, retrieval_service, cases) -> None:
    scores = []
    document_scores = []
    hit_scores = {1: [], 3: [], 5: []}
    reciprocal_ranks = []

    for case in cases:
        retrieved = retrieval_service.retrieve(case.question, top_k=5)
        retrieved_ids = [chunk.id for chunk in retrieved]
        case_score = recall_at_k(case, retrieved)
        document_scores.append(document_recall_at_k(case, retrieved))
        scores.append(case_score)
        for k in hit_scores:
            hit_scores[k].append(hit_at_k(case, retrieved, k))
        reciprocal_ranks.append(reciprocal_rank(case, retrieved))
        print(f"{label}_question={case.question}")
        print(f"{label}_retrieved={retrieved_ids}")
        print(f"{label}_recall={case_score:.3f}")

    print(f"{label}_recall_at_5={sum(scores) / len(scores):.3f}")
    print(f"{label}_document_recall_at_5={sum(document_scores) / len(document_scores):.3f}")
    for k, values in hit_scores.items():
        print(f"{label}_hit_at_{k}={sum(values) / len(values):.3f}")
    print(
        f"{label}_document_hit_at_5="
        f"{sum(document_hit_at_k(case, retrieval_service.retrieve(case.question, top_k=5), 5) for case in cases) / len(cases):.3f}"
    )
    print(f"{label}_mrr={sum(reciprocal_ranks) / len(reciprocal_ranks):.3f}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--corpus",
        choices=("curated", "fetched"),
        default="curated",
        help="Corpus and matching evaluation labels to benchmark.",
    )
    args = parser.parse_args()
    project_root = Path(__file__).resolve().parents[1]
    if args.corpus == "fetched":
        corpus_dir = project_root / "data" / "fetched_documents"
        documents = load_documents(corpus_dir, corpus_dir / "manifest.json")
        cases = load_evaluation_cases(project_root / "data" / "fetched_evaluation_cases.json")
    else:
        documents = load_documents(project_root / "data" / "documents")
        cases = load_evaluation_cases(project_root / "data" / "evaluation_cases.json")

    print(f"corpus={args.corpus} documents={len(documents)} cases={len(cases)}")

    embedding_service = EmbeddingService()
    chunker = TokenChunker()
    chunks = [chunk for document in documents for chunk in chunker.chunk(document)]
    vector_store = QdrantVectorStore(
        collection_name=f"wayfinder_baseline_{uuid4().hex}",
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

        retrieval_service = RetrievalService(embedding_service, vector_store)
        report_metrics("dense", retrieval_service, cases)
        hybrid_service = HybridRetrievalService(
            dense_retrieval=retrieval_service,
            lexical_retrieval=LexicalRetriever(chunks),
        )
        report_metrics("hybrid", hybrid_service, cases)
        reranked_service = RerankedRetrievalService(
            candidate_retrieval=hybrid_service,
            reranker=CrossEncoderReranker(),
            candidate_k=20,
        )
        report_metrics("reranked", reranked_service, cases)
    finally:
        vector_store.client.delete_collection(vector_store.collection_name)


if __name__ == "__main__":
    main()
