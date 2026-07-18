"""
mood_analysis.py
-----------------
Lightweight NLP utilities for the AI-Based Mental Health Monitoring Solution.

Uses TextBlob (rule/lexicon based) to score sentiment of a journal entry and
maps it to a human-friendly mood category. Also contains a small keyword
watchlist used to flag entries that may need extra care (e.g. mentions of
self-harm) so the app can surface crisis resources.

This is NOT a diagnostic or clinical tool. It is a self-awareness aid only.
"""

from __future__ import annotations
from dataclasses import dataclass
from textblob import TextBlob

# Keywords that should trigger a gentle safety prompt with helpline info.
# Kept intentionally short/high-level -- this is a safety net, not a
# clinical screening instrument.
_CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "self harm", "self-harm",
    "hurt myself", "want to die", "no reason to live", "can't go on",
]


@dataclass
class MoodResult:
    polarity: float          # -1 (very negative) to +1 (very positive)
    subjectivity: float      # 0 (objective/factual) to 1 (subjective/opinion)
    mood_label: str          # human readable bucket
    emoji: str                # matching emoji
    is_crisis_flag: bool      # True if crisis keywords detected


def _bucket_from_polarity(polarity: float) -> tuple[str, str]:
    """Map a -1..1 polarity score to a mood label + emoji."""
    if polarity <= -0.5:
        return "Very Low", "😢"
    if polarity <= -0.1:
        return "Low", "😕"
    if polarity < 0.1:
        return "Neutral", "😐"
    if polarity < 0.5:
        return "Good", "🙂"
    return "Very Good", "😄"


def analyze_entry(text: str) -> MoodResult:
    """Analyze a journal / mood entry and return a MoodResult."""
    text = text or ""
    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 3)
    subjectivity = round(blob.sentiment.subjectivity, 3)
    label, emoji = _bucket_from_polarity(polarity)

    lowered = text.lower()
    is_crisis = any(kw in lowered for kw in _CRISIS_KEYWORDS)

    return MoodResult(
        polarity=polarity,
        subjectivity=subjectivity,
        mood_label=label,
        emoji=emoji,
        is_crisis_flag=is_crisis,
    )


def mood_score_to_10(polarity: float) -> int:
    """Convert -1..1 polarity into a friendlier 0..10 wellbeing score."""
    return round((polarity + 1) * 5)
