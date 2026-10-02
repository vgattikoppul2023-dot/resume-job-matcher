# AI-Powered Resume / Job Matching System

An NLP matching engine that scores how well a resume fits a job posting and recommends the best-matching jobs in real time. Built with **Python, Flask, and scikit-learn** (TF-IDF + cosine similarity), containerized with **Docker**, and tested on every push with **GitHub Actions**.

## How it works

1. **Clean** — text is lowercased, punctuation is stripped, and common skill aliases are normalized (`k8s` → `kubernetes`, `js` → `javascript`).
2. **Vectorize** — job postings are turned into TF-IDF vectors using unigrams and bigrams, so phrases like *spring boot* and *machine learning* count as single skills.
3. **Score** — a resume is vectorized the same way and compared to every job with cosine similarity.
4. **Explain** — each match returns the shared terms that drove the score.

## API

| Method | Path | Body | Returns |
|---|---|---|---|
| `POST` | `/api/match` | `{"resume": "...", "top_k": 5}` | Ranked jobs with scores and matched terms |
| `POST` | `/api/score` | `{"resume": "...", "job": "..."}` | One match score (0–1) and matched terms |
| `GET` | `/health` | — | Service status |

Example:

```bash
curl -X POST localhost:5000/api/match -H "Content-Type: application/json" \
     -d '{"resume": "Java developer with Spring Boot, Kafka and AWS"}'
```

## Run locally

```bash
pip install -r requirements.txt
python -m app.main
```

Or with Docker:

```bash
docker build -t resume-job-matcher .
docker run -p 5000:5000 resume-job-matcher
```

## Test and evaluate

```bash
pytest -q
python -m app.evaluate data/labeled_pairs.json
```

`evaluate` reports top-1 and top-3 accuracy on a labeled set of resume → job pairs. Add your own pairs to `data/labeled_pairs.json` to measure accuracy on a larger sample.

## Project structure

```
app/
├── text.py       # cleaning + skill alias normalization
├── matcher.py    # TF-IDF + cosine similarity engine
├── main.py       # Flask REST API
└── evaluate.py   # accuracy evaluation on labeled pairs
data/             # sample jobs and labeled pairs
tests/            # pytest suite
.github/workflows # CI: tests, evaluation, Docker build
```
