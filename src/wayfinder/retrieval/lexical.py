from collections import Counter
from math import log
import re

from wayfinder.ingestion.models import Chunk


class LexicalRetriever:
    def __init__(
        self,
        chunks: list[Chunk],
        k1: float = 1.5,
        b: float = 0.75,
    ) -> None:
        if not chunks:
            raise ValueError("Lexical retriever requires at least one chunk")

        self.chunks = chunks
        self.k1 = k1
        self.b = b
        self.term_counts = [Counter(self._tokenize(chunk.content)) for chunk in chunks]
        self.document_frequency = Counter(
            term
            for counts in self.term_counts
            for term in counts
        )
        self.average_length = sum(
            sum(counts.values()) for counts in self.term_counts
        ) / len(self.term_counts)

    def search(self, query: str, top_k: int = 5) -> list[Chunk]:
        query_terms = self._tokenize(query)
        scored_chunks = [
            (self._score(query_terms, counts), index)
            for index, counts in enumerate(self.term_counts)
        ]
        scored_chunks.sort(key=lambda item: (-item[0], item[1]))
        return [self.chunks[index] for _, index in scored_chunks[:top_k]]

    def _score(self, query_terms: list[str], counts: Counter[str]) -> float:
        document_length = sum(counts.values())
        score = 0.0

        for term in query_terms:
            term_frequency = counts[term]
            if not term_frequency:
                continue

            document_count = self.document_frequency[term]
            idf = log(
                1 + (len(self.chunks) - document_count + 0.5)
                / (document_count + 0.5)
            )
            normalization = 1 - self.b + self.b * document_length / self.average_length
            score += idf * (
                term_frequency * (self.k1 + 1)
                / (term_frequency + self.k1 * normalization)
            )

        return score

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return re.findall(r"\b\w+\b", text.lower())
