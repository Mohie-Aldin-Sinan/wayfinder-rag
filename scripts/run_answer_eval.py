import json
import argparse
from pathlib import Path
from uuid import uuid4

from wayfinder.embeddings.service import EmbeddingService
from wayfinder.evaluation import (
    contains_expected_phrases,
    has_source_citation,
    is_refusal,
    LocalAnswerJudge,
    load_documents,
)
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", choices=("curated", "fetched"), default="curated")
    parser.add_argument("--judge", choices=("local", "openrouter", "none"), default="local")
    parser.add_argument("--judge-model", default="openrouter/free")
    args = parser.parse_args()
    project_root = Path(__file__).resolve().parents[1]
    if args.corpus == "fetched":
        corpus_dir = project_root / "data" / "fetched_documents"
        documents = load_documents(corpus_dir, corpus_dir / "manifest.json")
        cases_path = project_root / "data" / "fetched_answer_evaluation_cases.json"
    else:
        documents = load_documents(project_root / "data" / "documents")
        cases_path = project_root / "data" / "answer_evaluation_cases.json"
    cases = json.loads(
        cases_path.read_text()
    )
    print(f"corpus={args.corpus} documents={len(documents)} cases={len(cases)}")
    chunker = TokenChunker()
    chunks = [chunk for document in documents for chunk in chunker.chunk(document)]
    embedding_service = EmbeddingService()
    vector_store = QdrantVectorStore(
        collection_name=f"wayfinder_answer_eval_{uuid4().hex}",
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
        retrieval = RerankedRetrievalService(
            hybrid,
            CrossEncoderReranker(),
            candidate_k=20,
        )
        generator = LocalGenerationService()
        if args.judge == "local":
            judge = LocalAnswerJudge(generator.generator)
        elif args.judge == "openrouter":
            from wayfinder.evaluation import OpenRouterAnswerJudge

            judge = OpenRouterAnswerJudge(model=args.judge_model)
        else:
            judge = None
        correct = cited = refused = 0
        answerable_correct = answerable_total = 0
        refusal_correct = refusal_total = 0
        judge_scores = []

        for case in cases:
            retrieved = [] if case.get("expected_refusal") else retrieval.retrieve(
                case["question"],
                top_k=3,
            )
            answer = generator.generate(case["question"], retrieved)
            is_correct = (
                is_refusal(answer)
                if case.get("expected_refusal")
                else contains_expected_phrases(
                    answer,
                    case["expected_phrases"],
                )
            )
            has_citation = has_source_citation(answer, retrieved)
            citation_compliant = (
                not case["requires_citation"] or has_citation
            )
            correct += int(is_correct)
            cited += int(citation_compliant)
            refused += int(is_refusal(answer))
            if case.get("expected_refusal"):
                refusal_total += 1
                refusal_correct += int(is_correct)
            else:
                answerable_total += 1
                answerable_correct += int(is_correct)
            print(f"question={case['question']}")
            print(f"correct={is_correct} cited={has_citation}")
            print(f"answer={answer}")
            if retrieved and judge:
                try:
                    judge_result = judge.judge(case["question"], answer, retrieved)
                    judge_scores.append(judge_result)
                    print(f"judge={judge_result}")
                except (ValueError, KeyError, TypeError) as error:
                    print(f"judge_error={error}")

        print(f"answer_correctness={correct / len(cases):.3f}")
        print(f"answerable_correctness={answerable_correct / answerable_total:.3f}")
        print(f"refusal_correctness={refusal_correct / refusal_total:.3f}")
        print(f"answer_citation_rate={cited / len(cases):.3f}")
        print(f"answer_refusal_rate={refused / len(cases):.3f}")
        if judge_scores:
            for field in ("faithfulness", "relevance", "citation_quality", "conciseness"):
                average = sum(float(score[field]) for score in judge_scores) / len(judge_scores)
                print(f"judge_{field}_average={average:.3f}")
    finally:
        vector_store.client.delete_collection(vector_store.collection_name)


if __name__ == "__main__":
    main()
