from collections.abc import Sequence

from wayfinder.ingestion.models import Chunk


def has_source_citation(answer: str, chunks: Sequence[Chunk]) -> bool:
    return any(f"[Source: {chunk.id}]" in answer for chunk in chunks)


def contains_expected_phrases(
    answer: str,
    expected_phrases: Sequence[str],
) -> bool:
    normalized_answer = answer.casefold()
    return all(phrase.casefold() in normalized_answer for phrase in expected_phrases)


def is_refusal(answer: str) -> bool:
    refusal_phrases = (
        "not enough information",
        "don't have enough information",
        "insufficient information",
        "cannot answer",
        "don't know",
        "do not know",
    )
    normalized_answer = answer.casefold()
    return any(phrase in normalized_answer for phrase in refusal_phrases)
