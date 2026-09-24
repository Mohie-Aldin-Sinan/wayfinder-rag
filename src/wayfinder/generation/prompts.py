from wayfinder.ingestion.models import Chunk


NOISE_PHRASES = (
    "want to see it in action",
    "create a free account",
    "interactive example project",
    "skip to content",
    "skip to main",
)


def clean_context(text: str) -> str:
    lines = []
    seen = set()
    for line in text.splitlines():
        normalized = " ".join(line.split())
        if not normalized:
            continue
        lowered = normalized.casefold()
        if any(phrase in lowered for phrase in NOISE_PHRASES):
            continue
        if normalized.count("🚀") >= 1:
            continue
        if normalized.casefold() in seen:
            continue
        seen.add(normalized.casefold())
        lines.append(normalized)
    return "\n".join(lines)


def build_grounded_prompt(query: str, chunks: list[Chunk]) -> str:
    context = "\n\n".join(
        f"[Source: {chunk.id}]\n{clean_context(chunk.content)}" for chunk in chunks
    )

    return (
        "Answer the question using only the provided context. "
        "If the context does not contain enough information, say so clearly. "
        "Ignore navigation menus, advertisements, signup prompts, repeated headings, and unrelated code examples. "
        "Give a direct answer in 1-3 sentences. Cite supporting sources using their source IDs.\n\n"
        f"Question:\n{query}\n\n"
        f"Context:\n{context}"
    )


def attach_source_citations(answer: str, chunks: list[Chunk]) -> str:
    if not chunks:
        return answer

    citations = " ".join(f"[Source: {chunk.id}]" for chunk in chunks)
    return f"{answer.rstrip()}\n\nSources: {citations}"
