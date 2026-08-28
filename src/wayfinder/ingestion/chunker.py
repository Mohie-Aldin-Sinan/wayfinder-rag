from tiktoken import get_encoding

from wayfinder.ingestion.models import Chunk, Document


class TokenChunker:
    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 50,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")

        if overlap < 0:
            raise ValueError("overlap cannot be negative")

        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.overlap = overlap
        self._tokenizer = get_encoding("cl100k_base")

    def chunk(self, document: Document) -> list[Chunk]:
        tokens = self._tokenizer.encode(document.content)

        step = self.chunk_size - self.overlap

        chunks: list[Chunk] = []

        for index, start in enumerate(range(0, len(tokens), step)):
            chunk_tokens = tokens[start : start + self.chunk_size]

            if not chunk_tokens:
                break

            content = self._tokenizer.decode(chunk_tokens)

            chunks.append(
                Chunk(
                    id=f"{document.id}-chunk-{index}",
                    document_id=document.id,
                    content=content,
                    chunk_index=index,
                    metadata=document.metadata.copy(),
                )
            )

        return chunks