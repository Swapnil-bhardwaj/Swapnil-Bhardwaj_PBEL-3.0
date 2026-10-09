"""
mood_analysis.py
-----------------
NLP utilities for the Student Mental Health & Mood Journal.

Uses TextBlob sentiment analysis to estimate mood polarity and subjectivity,
mapped to relatable student-centric emotional reflections and safety flags.

This is a peer-oriented self-awareness aid, NOT a clinical diagnostic tool.
"""

from __future__ import annotations
from dataclasses import dataclass
from textblob import TextBlob

# Safety keywords that surface empathetic crisis resources
_CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "self harm", "self-harm",
    "hurt myself", "want to die", "no reason to live", "can't go on",
]


@dataclass
class MoodResult:
    polarity: float          # -1 (draining/difficult) to +1 (energized/positive)
    subjectivity: float      # 0 (objective facts) to 1 (emotional expression)
    mood_label: str          # human readable bucket
    emoji: str                # matching emoji
    is_crisis_flag: bool      # True if crisis keywords detected
    student_reflection: str   # Empathetic peer advice tailored to the score


def _bucket_from_polarity(polarity: float) -> tuple[str, str, str]:
    """Map a -1..1 polarity score to a mood label, emoji, and peer note."""
    if polarity <= -0.5:
        return (
            "Exhausted / Low",
            "🌧️",
            "You are carrying a really heavy emotional load today. Be gentle with yourself. Step away from your desk, postpone non-urgent tasks, and consider reaching out to a close friend or counselor.",
        )
    if polarity <= -0.1:
        return (
            "Drained / Stressed",
            "☁️",
            "Sounds like college pressure or life is taking a toll right now. You don't have to conquer everything today — taking a 15-minute breather or taking a nap is completely valid.",
        )
    if polarity < 0.15:
        return (
            "Steady / Grounded",
            "🌤️",
            "A balanced, level-headed headspace. A solid foundation for calm studying or taking a guilt-free evening off.",
        )
    if polarity < 0.55:
        return (
            "Upbeat / Good Vibe",
            "✨",
            "Nice energy today! Celebrate the small wins, whether it was getting through a tough lecture or finishing a problem set.",
        )
    return (
        "Thriving / Energized",
        "🌟",
        "Amazing vibe! You're in a great space right now. Bottle this feeling up and remember it next time exam stress tries to get in your head.",
    )


def analyze_entry(text: str) -> MoodResult:
    """Analyze a journal / mood entry and return a student-tailored MoodResult."""
    text = text or ""
    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 3)
    subjectivity = round(blob.sentiment.subjectivity, 3)
    label, emoji, note = _bucket_from_polarity(polarity)

    lowered = text.lower()
    is_crisis = any(kw in lowered for kw in _CRISIS_KEYWORDS)

    return MoodResult(
        polarity=polarity,
        subjectivity=subjectivity,
        mood_label=label,
        emoji=emoji,
        is_crisis_flag=is_crisis,
        student_reflection=note,
    )


def mood_score_to_10(polarity: float) -> int:
    """Convert -1..1 polarity into a student wellbeing score from 0 to 10."""
    return round((polarity + 1) * 5)
