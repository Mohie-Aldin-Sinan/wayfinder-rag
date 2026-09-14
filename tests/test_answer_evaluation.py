from wayfinder.evaluation import (
    contains_expected_phrases,
    has_source_citation,
    is_refusal,
)
from wayfinder.ingestion.models import Chunk


def test_answer_evaluation_checks_citations_and_expected_facts():
    chunks = [Chunk(
        id="chunk-1",
        document_id="doc-1",
        content="Hybrid retrieval combines vector and lexical search.",
        chunk_index=0,
    )]
    answer = "It combines vector and lexical search. [Source: chunk-1]"

    assert has_source_citation(answer, chunks)
    assert contains_expected_phrases(answer, ["vector", "lexical"])
    assert not is_refusal(answer)


def test_answer_evaluation_detects_refusal():
    assert is_refusal("There is not enough information in the context.")
