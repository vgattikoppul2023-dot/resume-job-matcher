"""Measures matching accuracy on a labeled set: is the correct job in the top-k results?

Usage: python -m app.evaluate data/labeled_pairs.json
Each item: {"resume": "...", "expected_job_id": "..."}
"""
import json
import sys
from pathlib import Path

from .main import DATA_PATH
from .matcher import Matcher


def evaluate(pairs: list[dict], jobs: list[dict], k: int = 3) -> dict:
    matcher = Matcher(jobs)
    top1 = topk = 0
    for p in pairs:
        ids = [m.id for m in matcher.rank(p["resume"], k)]
        top1 += ids[0] == p["expected_job_id"]
        topk += p["expected_job_id"] in ids
    n = len(pairs)
    return {"samples": n, "top1_accuracy": round(top1 / n, 3), f"top{k}_accuracy": round(topk / n, 3)}


if __name__ == "__main__":
    pairs = json.loads(Path(sys.argv[1]).read_text())
    jobs = json.loads(DATA_PATH.read_text())
    print(json.dumps(evaluate(pairs, jobs), indent=2))
