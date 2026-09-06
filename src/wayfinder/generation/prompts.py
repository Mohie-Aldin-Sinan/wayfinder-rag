from wayfinder.ingestion.models import Chunk


def build_grounded_prompt(query: str, chunks: list[Chunk]) -> str:
    context = "\n\n".join(
        f"[Source: {chunk.id}]\n{chunk.content}" for chunk in chunks
    )

    return (
        "Answer the question using only the provided context. "
        "If the context does not contain enough information, say so clearly. "
        "Cite supporting sources using their source IDs.\n\n"
        f"Question:\n{query}\n\n"
        f"Context:\n{context}"
    )
