from app.main import create_app
from app.matcher import Matcher
from app.text import clean

JOBS = [
    {"id": "java", "title": "Java Dev", "text": "Java Spring Boot Kafka microservices"},
    {"id": "react", "title": "React Dev", "text": "React JavaScript CSS frontend"},
]


def test_clean_normalizes_aliases():
    assert "kubernetes" in clean("Deployed on K8s")
    assert "javascript" in clean("JS and HTML")


def test_matcher_ranks_best_job_first():
    results = Matcher(JOBS).rank("I build Spring Boot services with Kafka", top_k=2)
    assert results[0].id == "java"
    assert results[0].score > results[1].score


def test_match_endpoint():
    client = create_app(JOBS).test_client()
    res = client.post("/api/match", json={"resume": "React and CSS developer"})
    assert res.status_code == 200
    assert res.get_json()["matches"][0]["id"] == "react"


def test_match_requires_resume():
    client = create_app(JOBS).test_client()
    assert client.post("/api/match", json={}).status_code == 400


def test_score_endpoint():
    client = create_app(JOBS).test_client()
    res = client.post("/api/score", json={"resume": "Java Kafka", "job": "Java Kafka Spring"})
    assert res.status_code == 200
    assert 0 < res.get_json()["score"] <= 1
