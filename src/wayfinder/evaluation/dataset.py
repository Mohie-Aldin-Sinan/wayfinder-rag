import json
from pathlib import Path

from wayfinder.evaluation.models import RetrievalEvaluationCase
from wayfinder.ingestion.models import Document


def load_documents(directory: Path) -> list[Document]:
    return [
        Document(
            id=path.stem,
            content=path.read_text(encoding="utf-8"),
            metadata={"source": str(path)},
        )
        for path in sorted(directory.glob("*.md"))
    ]


def load_evaluation_cases(path: Path) -> list[RetrievalEvaluationCase]:
    raw_cases = json.loads(path.read_text(encoding="utf-8"))

    return [
        RetrievalEvaluationCase(
            question=case["question"],
            relevant_chunk_ids=frozenset(case["relevant_chunk_ids"]),
        )
        for case in raw_cases
    ]
