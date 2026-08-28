import pytest
from pydantic import ValidationError

from wayfinder.ingestion.chunker import TokenChunker
from wayfinder.ingestion.models import Chunk, Document


def test_document_accepts_content_and_metadata():
    document = Document(
        id="doc-1",
        content="Qdrant supports vector search.",
        metadata={
            "source": "qdrant",
            "source_type": "documentation",
        },
    )

    assert document.content == "Qdrant supports vector search."
    assert document.metadata["source_type"] == "documentation"


def test_document_rejects_empty_content():
    with pytest.raises(ValidationError):
        Document(content="")

def test_chunk_preserves_document_provenance():
    chunk = Chunk(
        id="doc-1-chunk-0",
        document_id="doc-1",
        content="Qdrant supports filtering.",
        chunk_index=0,
        metadata={
            "source_type": "documentation",
            "title": "Filtering",
        },
    )

    assert chunk.document_id == "doc-1"
    assert chunk.chunk_index == 0
    assert chunk.metadata["source_type"] == "documentation"



def test_chunker_rejects_invalid_configuration():
    with pytest.raises(ValueError):
        TokenChunker(chunk_size=0)

    with pytest.raises(ValueError):
        TokenChunker(chunk_size=100, overlap=100)

    with pytest.raises(ValueError):
        TokenChunker(chunk_size=100, overlap=101)

    with pytest.raises(ValueError):
        TokenChunker(chunk_size=100, overlap=-1)

def test_short_document_produces_one_chunk():
    document = Document(
        id="doc-1",
        content="Qdrant is a vector database.",
        metadata={"source_type": "documentation"},
    )

    chunker = TokenChunker(chunk_size=100, overlap=10)

    chunks = chunker.chunk(document)

    assert len(chunks) == 1
    assert chunks[0].document_id == "doc-1"
    assert chunks[0].chunk_index == 0
    assert chunks[0].content == document.content
    assert chunks[0].metadata == document.metadata