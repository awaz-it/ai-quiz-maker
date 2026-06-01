"""
quiz_generator.py

Generates simple quizzes (MCQ, True/False, Fill-in-the-blank)
from plain lecture notes using lightweight NLP heuristics.

This intentionally avoids heavy ML models and uses rules based on
sentence/keyword extraction from `utils.py`.
"""
from typing import List, Dict, Tuple
import random
import re

try:
    from .utils import extract_sentences, extract_keywords, clean_text
except ImportError:
    from utils import extract_sentences, extract_keywords, clean_text


def _choose_items(seq, n):
    if not seq:
        return []
    if len(seq) <= n:
        # return a shuffled copy
        s = list(seq)
        random.shuffle(s)
        return s
    return random.sample(seq, n)


def generate_mcq(text: str, count: int = 5) -> List[Dict]:
    """Generate simple MCQs.

    Each MCQ is a dict with:
    - question: text with the key word replaced by a blank
    - options: list of 4 answer strings
    - answer: index (0-3) of the correct option
    """
    text = clean_text(text)
    sentences = extract_sentences(text)
    keywords = extract_keywords(text, top_n=20)

    mcqs = []
    if not sentences or not keywords:
        return mcqs

    # For candidates, prefer sentences that contain a keyword
    candidates: List[Tuple[str, str]] = []  # (sentence, keyword)
    for kw in keywords:
        pattern = re.compile(re.escape(kw), re.IGNORECASE)
        for s in sentences:
            if pattern.search(s):
                candidates.append((s, kw))

    # Fallback: pair top keywords with random sentences
    if not candidates:
        for kw in keywords:
            candidates.append((random.choice(sentences), kw))

    chosen = _choose_items(candidates, count)

    for sent, kw in chosen:
        # Create a blanked question
        # Replace only the first occurrence of the keyword (case-insensitive)
        def _repl(m):
            return '_____'

        q_text = re.sub(re.escape(kw), _repl, sent, flags=re.IGNORECASE, count=1)

        # Build options: correct + 3 distractors from other keywords or nouns
        distract_pool = [k for k in keywords if k.lower() != kw.lower()]
        distractors = _choose_items(distract_pool, 3)
        # If not enough distractors, create simple synthetic ones
        while len(distractors) < 3:
            fake = f"{kw} {random.choice(['type','form','kind'])}"
            if fake not in distractors:
                distractors.append(fake)

        options = [kw] + distractors
        random.shuffle(options)
        answer_idx = options.index(kw)

        mcqs.append({
            "question": q_text,
            "options": options,
            "answer": answer_idx,
        })

    return mcqs


def generate_true_false(text: str, count: int = 5) -> List[Dict]:
    """Generate True/False statements.

    Strategy:
    - Pick informative sentences
    - For some of them, make them false by swapping a keyword with another
    """
    text = clean_text(text)
    sentences = extract_sentences(text)
    keywords = extract_keywords(text, top_n=30)

    tf = []
    if not sentences:
        return tf

    chosen_sentences = _choose_items(sentences, count)

    for s in chosen_sentences:
        # Decide randomly whether to flip (make false)
        make_false = random.random() < 0.4  # ~40% false
        statement = s
        truth = True

        if make_false and keywords:
            # Try to replace a keyword in the sentence with a different keyword
            for kw in keywords:
                if re.search(re.escape(kw), s, re.IGNORECASE):
                    # pick a replacement different from kw
                    repl_candidates = [k for k in keywords if k.lower() != kw.lower()]
                    if repl_candidates:
                        repl = random.choice(repl_candidates)
                        statement = re.sub(re.escape(kw), repl, s, flags=re.IGNORECASE, count=1)
                        truth = False
                    break

        tf.append({
            "statement": statement,
            "answer": truth,
        })

    return tf


def generate_fill_blank(text: str, count: int = 5) -> List[Dict]:
    """Generate fill-in-the-blank questions by blanking keywords inside sentences."""
    text = clean_text(text)
    sentences = extract_sentences(text)
    keywords = extract_keywords(text, top_n=30)

    blanks = []
    if not sentences or not keywords:
        return blanks

    # Find sentence-keyword pairs
    pairs = []
    for kw in keywords:
        pattern = re.compile(re.escape(kw), re.IGNORECASE)
        for s in sentences:
            if pattern.search(s):
                pairs.append((s, kw))

    if not pairs:
        # fallback: pair top keywords with a random sentence
        for kw in keywords[:count]:
            pairs.append((random.choice(sentences), kw))

    chosen = _choose_items(pairs, count)

    for sent, kw in chosen:
        question = re.sub(re.escape(kw), '_____', sent, flags=re.IGNORECASE, count=1)
        blanks.append({
            "question": question,
            "answer": kw,
        })

    return blanks
