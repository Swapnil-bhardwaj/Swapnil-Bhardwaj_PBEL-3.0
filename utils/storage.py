"""
storage.py
----------
Very small CSV-backed storage layer so mood logs and quiz results survive
between sessions without needing a database. Fine for a college project /
single-user demo. Swap for SQLite/Postgres if you want multi-user support.
"""

from __future__ import annotations
import os
import pandas as pd
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
MOOD_LOG_PATH = os.path.join(DATA_DIR, "mood_log.csv")
QUIZ_LOG_PATH = os.path.join(DATA_DIR, "quiz_log.csv")

os.makedirs(DATA_DIR, exist_ok=True)


def _ensure_csv(path: str, columns: list[str]) -> None:
    if not os.path.exists(path):
        pd.DataFrame(columns=columns).to_csv(path, index=False)


def log_mood(entry_text: str, polarity: float, subjectivity: float, mood_label: str) -> None:
    _ensure_csv(MOOD_LOG_PATH, ["timestamp", "entry", "polarity", "subjectivity", "mood_label"])
    df = pd.read_csv(MOOD_LOG_PATH)
    new_row = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "entry": entry_text,
        "polarity": polarity,
        "subjectivity": subjectivity,
        "mood_label": mood_label,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(MOOD_LOG_PATH, index=False)


def load_mood_log() -> pd.DataFrame:
    _ensure_csv(MOOD_LOG_PATH, ["timestamp", "entry", "polarity", "subjectivity", "mood_label"])
    df = pd.read_csv(MOOD_LOG_PATH)
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def log_quiz(quiz_name: str, score: int, max_score: int, severity: str) -> None:
    _ensure_csv(QUIZ_LOG_PATH, ["timestamp", "quiz_name", "score", "max_score", "severity"])
    df = pd.read_csv(QUIZ_LOG_PATH)
    new_row = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "quiz_name": quiz_name,
        "score": score,
        "max_score": max_score,
        "severity": severity,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(QUIZ_LOG_PATH, index=False)


def load_quiz_log() -> pd.DataFrame:
    _ensure_csv(QUIZ_LOG_PATH, ["timestamp", "quiz_name", "score", "max_score", "severity"])
    df = pd.read_csv(QUIZ_LOG_PATH)
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def clear_all_data() -> None:
    """Wipe local logs (used by a 'reset my data' button in the UI)."""
    for path in (MOOD_LOG_PATH, QUIZ_LOG_PATH):
        if os.path.exists(path):
            os.remove(path)
