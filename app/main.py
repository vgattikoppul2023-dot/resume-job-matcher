"""Flask REST API serving match scores and recommendations in real time."""
import json
import os
from dataclasses import asdict
from pathlib import Path

from flask import Flask, jsonify, request

from .matcher import Matcher

DATA_PATH = Path(os.getenv("JOBS_PATH", Path(__file__).parent.parent / "data" / "jobs.json"))


def create_app(jobs: list[dict] | None = None) -> Flask:
    app = Flask(__name__)
    jobs = jobs if jobs is not None else json.loads(DATA_PATH.read_text())
    matcher = Matcher(jobs)

    @app.get("/health")
    def health():
        return {"status": "ok", "jobs_indexed": len(jobs)}

    @app.post("/api/match")
    def match():
        body = request.get_json(silent=True) or {}
        resume = (body.get("resume") or "").strip()
        if not resume:
            return jsonify(error="'resume' text is required"), 400
        top_k = max(1, min(int(body.get("top_k", 5)), 20))
        return jsonify(matches=[asdict(m) for m in matcher.rank(resume, top_k)])

    @app.post("/api/score")
    def score():
        body = request.get_json(silent=True) or {}
        resume, job = body.get("resume", ""), body.get("job", "")
        if not resume.strip() or not job.strip():
            return jsonify(error="'resume' and 'job' text are required"), 400
        single = Matcher([{"id": "job", "title": "job", "text": job}])
        result = single.rank(resume, 1)[0]
        return jsonify(score=result.score, matched_terms=result.matched_terms)

    return app


app = create_app() if DATA_PATH.exists() else None

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
