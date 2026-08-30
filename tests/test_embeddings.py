from unittest.mock import MagicMock

import numpy as np

from wayfinder.embeddings.service import EmbeddingService


def test_embed_returns_single_vector():
    service = EmbeddingService.__new__(EmbeddingService)

    fake_model = MagicMock()
    fake_model.encode.return_value = np.array([0.1, 0.2, 0.3])

    service.model = fake_model
    service.batch_size = 32

    result = service.embed("hello")

    assert result == [0.1, 0.2, 0.3]

    fake_model.encode.assert_called_once_with(
        "hello",
        normalize_embeddings=True,
    )


def test_embed_many_returns_one_vector_per_text():
    service = EmbeddingService.__new__(EmbeddingService)

    fake_model = MagicMock()
    fake_model.encode.return_value = np.array(
        [
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6],
        ]
    )

    service.model = fake_model
    service.batch_size = 32

    texts = ["hello", "world"]

    result = service.embed_many(texts)

    assert len(result) == 2
    assert result[0] == [0.1, 0.2, 0.3]
    assert result[1] == [0.4, 0.5, 0.6]

    fake_model.encode.assert_called_once_with(
        texts,
        batch_size=32,
        normalize_embeddings=True,
    )