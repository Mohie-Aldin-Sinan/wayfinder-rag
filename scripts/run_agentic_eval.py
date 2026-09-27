import json
from pathlib import Path
from uuid import uuid4

from wayfinder.embeddings.service import EmbeddingService
from wayfinder.evaluation import document_recall_at_k, recall_at_k
from wayfinder.evaluation.models import RetrievalEvaluationCase
from wayfinder.evaluation.dataset import load_documents
from wayfinder.indexing.service import IndexingService
from wayfinder.ingestion.chunker import TokenChunker
from wayfinder.retrieval.agentic import AgenticRetrievalService
from wayfinder.retrieval.agentic_llm import HybridSufficiencyChecker, OpenRouterContextChecker, OpenRouterQueryRewriter
from wayfinder.retrieval.hybrid import HybridRetrievalService
from wayfinder.retrieval.lexical import LexicalRetriever
from wayfinder.retrieval.qdrant_store import QdrantVectorStore
from wayfinder.retrieval.reranked import RerankedRetrievalService
from wayfinder.retrieval.reranker import CrossEncoderReranker
from wayfinder.retrieval.service import RetrievalService
from wayfinder.observability import TraceRecorder


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    corpus = root / "data" / "fetched_documents"
    documents = load_documents(corpus, corpus / "manifest.json")
    raw_cases = json.loads((root / "data" / "agentic_evaluation_cases.json").read_text())
    cases = [
        RetrievalEvaluationCase(
            question=case["question"],
            relevant_chunk_ids=frozenset(case["relevant_chunk_ids"]),
        )
        for case in raw_cases
    ]
    embedding = EmbeddingService()
    chunker = TokenChunker()
    chunks = [chunk for document in documents for chunk in chunker.chunk(document)]
    store = QdrantVectorStore(
        collection_name=f"wayfinder_agentic_{uuid4().hex}",
        vector_size=len(embedding.embed("dimension probe")),
    )
    try:
        indexer = IndexingService(chunker, embedding, store)
        for document in documents:
            indexer.index(document)
        dense = RetrievalService(embedding, store)
        hybrid = HybridRetrievalService(dense, LexicalRetriever(chunks))
        reranked = RerankedRetrievalService(hybrid, CrossEncoderReranker(), candidate_k=20)
        trace_path = Path("/tmp/wayfinder-agentic-eval.jsonl")
        if trace_path.exists():
            trace_path.unlink()
        agentic = AgenticRetrievalService(
            reranked,
            HybridSufficiencyChecker(OpenRouterContextChecker()),
            OpenRouterQueryRewriter(),
            max_attempts=2,
            trace_recorder=TraceRecorder(trace_path),
        )
        baseline_scores = []
        agentic_scores = []
        baseline_chunk_scores = []
        agentic_chunk_scores = []
        rewrites = 0
        attempts = []
        successful_retries = 0
        unnecessary_retries = 0
        failed_retries = 0
        for case in cases:
            baseline = reranked.retrieve(case.question, top_k=1)
            result = agentic.retrieve(case.question, top_k=1)
            baseline_score = document_recall_at_k(case, baseline)
            agentic_score = document_recall_at_k(case, result.chunks)
            baseline_scores.append(baseline_score)
            agentic_scores.append(agentic_score)
            baseline_chunk_scores.append(recall_at_k(case, baseline))
            agentic_chunk_scores.append(recall_at_k(case, result.chunks))
            rewrites += int(result.rewritten)
            attempts.append(result.attempts)
            if result.rewritten:
                if agentic_score > baseline_score:
                    successful_retries += 1
                elif agentic_score == baseline_score:
                    unnecessary_retries += 1
                else:
                    failed_retries += 1
            print(f"question={case.question}")
            print(f"baseline_document_recall={baseline_score:.3f}")
            print(f"baseline_chunk_recall={baseline_chunk_scores[-1]:.3f}")
            print(f"agentic_query={result.query}")
            print(f"agentic_document_recall={agentic_score:.3f}")
            print(f"agentic_chunk_recall={agentic_chunk_scores[-1]:.3f}")
            print(f"agentic_attempts={result.attempts}")
        print(f"baseline_document_recall_at_1={sum(baseline_scores) / len(baseline_scores):.3f}")
        print(f"agentic_document_recall_at_1={sum(agentic_scores) / len(agentic_scores):.3f}")
        print(f"baseline_chunk_recall_at_1={sum(baseline_chunk_scores) / len(baseline_chunk_scores):.3f}")
        print(f"agentic_chunk_recall_at_1={sum(agentic_chunk_scores) / len(agentic_chunk_scores):.3f}")
        print(f"agentic_rewrite_rate={rewrites / len(cases):.3f}")
        print(f"agentic_average_attempts={sum(attempts) / len(attempts):.3f}")
        print(f"successful_retries={successful_retries}")
        print(f"unnecessary_retries={unnecessary_retries}")
        print(f"failed_retries={failed_retries}")
        print("trace_path=/tmp/wayfinder-agentic-eval.jsonl")
    finally:
        store.client.delete_collection(store.collection_name)


if __name__ == "__main__":
    main()
