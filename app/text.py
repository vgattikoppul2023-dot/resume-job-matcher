"""Text cleaning shared by the matcher."""
import re

_SKILL_ALIASES = {
    r"\bjs\b": "javascript",
    r"\bk8s\b": "kubernetes",
    r"\bspringboot\b": "spring boot",
    r"\bpostgres\b": "postgresql",
    r"\bml\b": "machine learning",
    r"\baws\b": "aws",
}


def clean(text: str) -> str:
    """Lowercase, normalize common skill aliases, and strip punctuation."""
    text = text.lower()
    for pattern, replacement in _SKILL_ALIASES.items():
        text = re.sub(pattern, replacement, text)
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()
