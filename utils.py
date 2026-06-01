"""
utils.py

Helper functions for the AI Quiz Maker from Notes project.

Provides basic text cleaning, sentence extraction and keyword extraction
using NLTK. This is intentionally simple and beginner-friendly.
"""
from typing import List
import re
import nltk

# Ensure required NLTK resources are available. At runtime the script
# will attempt to download them if missing. This keeps the project
# beginner-friendly: first run may download resources.
_NLTK_RESOURCES = ["punkt", "averaged_perceptron_tagger", "stopwords"]

def ensure_nltk_resources():
    for res in _NLTK_RESOURCES:
        try:
            nltk.data.find(res)
        except LookupError:
            nltk.download(res)


def clean_text(text: str) -> str:
    """Return a lightly cleaned copy of the input text.

    - Normalizes whitespace
    - Strips leading/trailing spaces
    """
    if not isinstance(text, str):
        return ""
    # Replace multiple whitespace with single space
    t = re.sub(r"\s+", " ", text)
    return t.strip()


def extract_sentences(text: str) -> List[str]:
    """Split text into sentences using NLTK's sentence tokenizer."""
    ensure_nltk_resources()
    text = clean_text(text)
    if not text:
        return []
    return nltk.sent_tokenize(text)


def extract_keywords(text: str, top_n: int = 10) -> List[str]:
    """Return a list of candidate keywords (nouns) sorted by frequency.

    This uses a simple frequency count over nouns (NN, NNP etc.) and
    filters out English stopwords and single-character tokens.
    """
    ensure_nltk_resources()
    from nltk.corpus import stopwords
    from nltk import pos_tag, word_tokenize

    stop = set(stopwords.words("english"))

    text = clean_text(text)
    if not text:
        return []

    tokens = [w for w in word_tokenize(text) if re.search(r"[A-Za-z0-9]", w)]
    # POS tag tokens
    tagged = pos_tag(tokens)

    # Keep nouns and proper nouns
    noun_tags = {"NN", "NNS", "NNP", "NNPS"}
    candidates = [w for w, tag in tagged if tag in noun_tags]

    # normalize and filter stopwords and short tokens
    normalized = [w.lower() for w in candidates if w.lower() not in stop and len(w) > 1]

    # frequency
    freq = {}
    for w in normalized:
        freq[w] = freq.get(w, 0) + 1

    # sort by frequency
    sorted_words = sorted(freq.items(), key=lambda kv: kv[1], reverse=True)
    keywords = [w for w, _ in sorted_words]

    # return up to top_n unique keywords, title-cased for presentation
    unique = []
    for k in keywords:
        if k not in unique:
            unique.append(k)
        if len(unique) >= top_n:
            break

    return [u.title() for u in unique]
