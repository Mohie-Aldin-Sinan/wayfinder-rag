import json
import shutil
import tempfile
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen


BOILERPLATE_LINES = {
    "skip to main content",
    "skip to main",
    "documentation index",
    "table of contents",
    "on this page",
    "edit this page",
    "previous",
    "next",
}


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "nav", "footer", "svg"}:
            self.skip_depth += 1
        elif not self.skip_depth and tag in {"p", "h1", "h2", "h3", "li", "pre"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "nav", "footer", "svg"} and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip_depth and data.strip():
            self.parts.append(data.strip())


def fetch(url: str) -> str:
    request = Request(url, headers={"User-Agent": "Wayfinder-RAG/0.1"})
    with urlopen(request, timeout=30) as response:
        parser = TextExtractor()
        parser.feed(response.read().decode("utf-8", errors="replace"))
    return clean_text(parser.parts)


def clean_text(parts: list[str]) -> str:
    """Remove common documentation chrome without rewriting the article."""
    cleaned: list[str] = []
    previous = ""
    for part in parts:
        line = " ".join(part.split())
        if not line:
            continue
        normalized = line.casefold()
        if normalized in BOILERPLATE_LINES or normalized.startswith("fetch the complete documentation index"):
            continue
        if line == previous:
            continue
        cleaned.append(line)
        previous = line
    return "\n".join(cleaned)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "data" / "source_manifest.json").read_text())
    output_dir = root / "data" / "fetched_documents"
    output_dir.mkdir(parents=True, exist_ok=True)
    staging_dir = Path(tempfile.mkdtemp(prefix="wayfinder-corpus-", dir=output_dir.parent))
    records = []
    failures = []

    for source in manifest:
        for url in source["urls"]:
            document_id = f"{source['project'].lower().replace(' ', '-')}-{len(records)}"
            try:
                content = fetch(url)
            except Exception as error:
                failures.append({"project": source["project"], "source_url": url, "error": str(error)})
                continue

            if len(content.split()) < 50:
                failures.append({"project": source["project"], "source_url": url, "error": "extracted content is too short"})
                continue

            (staging_dir / f"{document_id}.md").write_text(content, encoding="utf-8")
            records.append({
                "id": document_id,
                "project": source["project"],
                "source_url": url,
                "fetched_at": datetime.now(timezone.utc).isoformat(),
            })

    if len(records) != len(list(staging_dir.glob("*.md"))):
        shutil.rmtree(staging_dir)
        raise RuntimeError("staged corpus is inconsistent; refusing to publish")

    for old_document in output_dir.glob("*.md"):
        old_document.unlink()
    for staged_document in staging_dir.glob("*.md"):
        shutil.move(str(staged_document), output_dir / staged_document.name)
    shutil.rmtree(staging_dir)

    (output_dir / "manifest.json").write_text(
        json.dumps({"documents": records, "failures": failures}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"fetched={len(records)} failed={len(failures)}")


if __name__ == "__main__":
    main()
