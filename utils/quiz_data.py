"""
quiz_data.py
------------
A short, original 10-question stress/wellbeing self-assessment.

IMPORTANT: This is inspired by the general *style* of standardized
wellbeing scales (Likert-scored, 0-3 per item) but the questions themselves
are original and this is explicitly a self-awareness tool, NOT a validated
clinical instrument (like the PHQ-9 or GAD-7) and must not be presented as
one. Always encourage professional consultation for real diagnosis.
"""

from __future__ import annotations

QUESTIONS = [
    "I have felt overwhelmed by my daily responsibilities.",
    "I have had trouble relaxing.",
    "I have felt irritable or easily annoyed.",
    "I have had difficulty falling or staying asleep.",
    "I have felt physically tense (tight shoulders, headaches, etc.).",
    "I have found it hard to concentrate on tasks.",
    "I have felt anxious or on edge without a clear reason.",
    "I have withdrawn from friends or activities I usually enjoy.",
    "I have felt low on energy or motivation.",
    "I have felt like things are piling up and I can't keep up.",
]

OPTIONS = [
    ("Not at all", 0),
    ("Several days", 1),
    ("More than half the days", 2),
    ("Nearly every day", 3),
]

MAX_SCORE = len(QUESTIONS) * 3  # 30


def score_to_severity(score: int) -> tuple[str, str]:
    """Return (severity_label, advice_text) for a given total score."""
    if score <= 7:
        return (
            "Low stress",
            "You seem to be managing well right now. Keep up whatever routines are working for you — "
            "regular sleep, movement, and downtime all help maintain this.",
        )
    if score <= 15:
        return (
            "Mild stress",
            "You're carrying some stress, which is very normal. Try the breathing exercise or one of the "
            "anti-stress games in this app, and consider building in short breaks through your day.",
        )
    if score <= 22:
        return (
            "Moderate stress",
            "Your stress levels look elevated. It may help to talk to someone you trust — a friend, family "
            "member, or counselor — about what's been going on, alongside small daily coping habits.",
        )
    return (
        "High stress",
        "Your responses suggest you're under significant stress right now. Please consider speaking with a "
        "mental health professional or counselor soon. If you ever feel unsafe or unable to cope, reach out "
        "to a helpline immediately (see the Chatbot tab for numbers).",
    )
