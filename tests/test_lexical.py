from wayfinder.ingestion.models import Chunk
from wayfinder.retrieval.lexical import LexicalRetriever


def test_lexical_retriever_prioritizes_exact_terms():
    chunks = [
        Chunk(
            id="general",
            document_id="doc",
            content="Retrieval uses context to answer questions.",
            chunk_index=0,
        ),
        Chunk(
            id="specific",
            document_id="doc",
            content="Hybrid retrieval helps with exact technical identifiers.",
            chunk_index=1,
        ),
    ]

    results = LexicalRetriever(chunks).search(
        "Which method helps exact technical identifiers?",
        top_k=1,
    )

    assert results[0].id == "specific"
