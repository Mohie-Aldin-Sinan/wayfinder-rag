from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(
        self,
        model_name: str = "Qwen/Qwen3-Embedding-0.6B",
        batch_size: int = 32,
    ):
        self.model = SentenceTransformer(model_name)
        self.batch_size = batch_size

    def embed(self, text: str) -> list[float]:
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            normalize_embeddings=True,
        )

        return embeddings.tolist()