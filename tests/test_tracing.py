import json
from pathlib import Path

from wayfinder.observability import TraceRecorder


def test_trace_recorder_appends_json_lines(tmp_path: Path):
    path = tmp_path / "trace.jsonl"
    recorder = TraceRecorder(path, run_id="run-1")

    recorder.record("retrieval", query="What is Qdrant?", top_k=3)
    recorder.record("generation", answer="A vector database.")

    events = [json.loads(line) for line in path.read_text().splitlines()]

    assert [event["event"] for event in events] == ["retrieval", "generation"]
    assert all(event["run_id"] == "run-1" for event in events)
    assert events[0]["top_k"] == 3
