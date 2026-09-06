from openai import OpenAI

from wayfinder.generation.prompts import build_grounded_prompt
from wayfinder.ingestion.models import Chunk


class GenerationService:
    def __init__(self, client: OpenAI, model: str) -> None:
        self.client = client
        self.model = model

    def generate(self, query: str, chunks: list[Chunk]) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=build_grounded_prompt(query, chunks),
        )
        return response.output_text
