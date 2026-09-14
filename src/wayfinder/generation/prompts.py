from wayfinder.ingestion.models import Chunk


def build_grounded_prompt(query: str, chunks: list[Chunk]) -> str:
    context = "\n\n".join(
        f"[Source: {chunk.id}]\n{chunk.content}" for chunk in chunks
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
