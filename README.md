# Wayfinder RAG

Wayfinder is a production-oriented retrieval-augmented generation system for open-source software knowledge. It is designed as an experimental RAG pipeline: each retrieval stage is modular, measurable, and replaceable.

## Pipeline

```text
documents
  -> token chunking
  -> local embeddings
  -> dense retrieval
  -> lexical BM25 retrieval
  -> reciprocal-rank fusion
  -> cross-encoder reranking
  -> grounded local generation
```

Retrieval and generation are deliberately separated. This makes it possible to measure whether an answer failed because the system found poor evidence or because the generator used good evidence poorly.

## Current Results

On the initial 14-question benchmark:

| Retriever | Hit@1 | MRR | Recall@5 |
| --- | ---: | ---: | ---: |
| Dense | 0.857 | 0.917 | 1.000 |
| Hybrid | 0.929 | 0.964 | 1.000 |
| Hybrid + reranking | 1.000 | 1.000 | 1.000 |

These results are an early benchmark, not a universal claim. The corpus is intentionally small and is still being expanded.

## Local Setup

The project uses local models and does not require a paid LLM API. Start the Qdrant container used by the integration tests:

```bash
docker start wayfinder-qdrant
uv sync
```

Run tests:

```bash
uv run pytest -q
```

Run the retrieval comparison:

```bash
uv run python scripts/run_baseline.py
```

Run the local grounded-answer demo:

```bash
uv run python scripts/run_local_answer.py
```

Run answer evaluation:

```bash
uv run python scripts/run_answer_eval.py
```

The first run downloads the local embedding, reranking, and generation models from Hugging Face. No OpenAI API key is required for these experiments.

## Evaluation

Retrieval is evaluated with recall@k, hit@k, and mean reciprocal rank. Answer evaluation currently checks expected factual phrases, citation presence, and refusal when no evidence is available.

The benchmark is intentionally versioned in `data/`. Evaluation labels identify the chunks that contain answer-supporting evidence. Changes to chunk size, overlap, models, or corpus should be recorded because they affect reproducibility.

## Project Status

Implemented:

- document models and token chunking
- local embedding and Qdrant indexing
- dense retrieval
- BM25-style lexical retrieval
- hybrid retrieval with reciprocal-rank fusion
- local cross-encoder reranking
- grounded local generation
- retrieval and answer evaluation

Next improvements include a larger documentation corpus, selective citations, cleaner generation configuration, and latency measurements.
