import json
from pathlib import Path

from wayfinder.evaluation.models import RetrievalEvaluationCase
from wayfinder.ingestion.models import Document


def load_source_manifest(path: Path) -> list[dict[str, object]]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_documents(directory: Path, manifest_path: Path | None = None) -> list[Document]:
    manifest_by_id: dict[str, dict[str, object]] = {}
    if manifest_path and manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        records = manifest.get("documents", manifest) if isinstance(manifest, dict) else manifest
        manifest_by_id = {record["id"]: record for record in records}

    documents = []
    for path in sorted(directory.glob("*.md")):
        metadata: dict[str, object] = {"source": str(path)}
        metadata.update(manifest_by_id.get(path.stem, {}))
        documents.append(
            Document(
                id=path.stem,
                content=path.read_text(encoding="utf-8"),
                metadata=metadata,
            )
        )
    return documents


def load_evaluation_cases(path: Path) -> list[RetrievalEvaluationCase]:
    raw_cases = json.loads(path.read_text(encoding="utf-8"))

    return [
        RetrievalEvaluationCase(
            question=case["question"],
            relevant_chunk_ids=frozenset(case["relevant_chunk_ids"]),
        )
        for case in raw_cases
    ]
