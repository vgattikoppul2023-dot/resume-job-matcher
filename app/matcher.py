"""TF-IDF + cosine-similarity engine that ranks jobs against resumes (and vice versa)."""
from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .text import clean


@dataclass
class Match:
    id: str
    title: str
    score: float
    matched_terms: list


class Matcher:
    def __init__(self, documents: list[dict]):
        """documents: list of {"id", "title", "text"} — e.g. job postings."""
        if not documents:
            raise ValueError("Matcher needs at least one document")
        self.documents = documents
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),   # captures phrases like "spring boot", "machine learning"
            sublinear_tf=True,
            min_df=1,
        )
        self.matrix = self.vectorizer.fit_transform(clean(d["text"]) for d in documents)
        self.terms = self.vectorizer.get_feature_names_out()

    def rank(self, query_text: str, top_k: int = 5) -> list[Match]:
        """Return the top_k documents most similar to query_text."""
        query_vec = self.vectorizer.transform([clean(query_text)])
        scores = cosine_similarity(query_vec, self.matrix).ravel()
        order = scores.argsort()[::-1][:top_k]
        q_terms = set(query_vec.nonzero()[1])
        results = []
        for i in order:
            shared = q_terms & set(self.matrix[i].nonzero()[1])
            top_shared = sorted(shared, key=lambda t: -self.matrix[i, t])[:8]
            results.append(Match(
                id=self.documents[i]["id"],
                title=self.documents[i]["title"],
                score=round(float(scores[i]), 4),
                matched_terms=[self.terms[t] for t in top_shared],
            ))
        return results
