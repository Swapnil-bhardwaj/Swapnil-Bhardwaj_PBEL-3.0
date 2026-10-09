"""
quiz_data.py
------------
Student-tailored 10-question Academic Stress & Burnout Self-Assessment.

Designed around common student stressors: exams, late-night cramming,
group projects, screen fatigue, and imposter syndrome.

Scored on a 0-3 Likert scale (Total: 30).
Explicitly a self-awareness aid, NOT a clinical diagnosis.
"""

from __future__ import annotations

QUESTIONS = [
    "Feeling overwhelmed by upcoming assignments, exams, or project submissions.",
    "Trouble turning off racing thoughts when trying to sleep before early morning classes.",
    "Getting easily annoyed or impatient with group project members, roommates, or peers.",
    "Struggling to concentrate on lecture notes or textbooks without feeling mentally exhausted.",
    "Physical tension: tight shoulders from laptop hunching, headaches, or skipping meals.",
    "Feeling guilty or anxious whenever you take a break instead of studying.",
    "Excessive dread or anxiety regarding GPA, upcoming tests, or career placements.",
    "Isolating yourself from friends, campus events, or hobbies you usually enjoy.",
    "Relying heavily on excessive caffeine or energy drinks just to stay functional.",
    "Feeling like all your peers have everything figured out while you are falling behind (imposter syndrome).",
]

OPTIONS = [
    ("Rarely / Not at all", 0),
    ("Several days a week", 1),
    ("More than half the week", 2),
    ("Almost every single day", 3),
]

MAX_SCORE = len(QUESTIONS) * 3  # 30


def score_to_severity(score: int) -> tuple[str, str, str]:
    """Return (severity_label, advice_text, badge_color) for a given total score."""
    if score <= 8:
        return (
            "Low Academic Stress 🌿",
            "You are navigating this semester with great resilience and balance! "
            "Keep protecting your sleep schedule, eating regular meals, and giving yourself downtime without guilt.",
            "#10B981",
        )
    if score <= 16:
        return (
            "Moderate College Hustle ⚡",
            "You are feeling the typical student squeeze. Deadlines and coursework are starting to pile up. "
            "Try scheduling focused 25-minute study blocks followed by 5-minute screen-free breaks. Don't sacrifice sleep for extra study time.",
            "#F59E0B",
        )
    if score <= 23:
        return (
            "Elevated Academic Burnout ⚠️",
            "Your stress levels are significantly elevated. It is likely affecting your focus, mood, and sleep. "
            "Step back: prioritize only your top 2 urgent tasks, speak to a friend or academic advisor, and schedule an evening completely off to reset your nervous system.",
            "#F97316",
        )
    return (
        "High Burnout / Overload Alert 🚨",
        "Your responses show you are carrying an unsustainable amount of pressure right now. "
        "Academic deadlines and GPA can always be managed, but your mental and physical health must come first. "
        "Please speak with someone you trust today — a campus counselor, student advisor, or family member. Check the MindMate Buddy page for immediate, free confidential support.",
        "#EF4444",
    )
