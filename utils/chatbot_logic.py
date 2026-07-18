"""
chatbot_logic.py
-----------------
A small rule/keyword based supportive chatbot ("MindMate"). It is NOT a
therapist and does not attempt to diagnose. It reflects feelings back,
offers gentle coping suggestions, and -- most importantly -- recognizes a
short list of crisis-related phrases and responds with helpline
information instead of generic chit-chat.

Design note: keeping this rule-based (rather than a trained model) keeps
the project dependency-light and fully explainable, which is usually what
a college-level "AI mental health" project is graded on.
"""

from __future__ import annotations
import random

CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "self harm", "self-harm",
    "hurt myself", "want to die", "no reason to live", "can't go on",
]

CRISIS_RESPONSE = (
    "I'm really sorry you're feeling this way. You deserve support from a real "
    "person right now, not just an app. Please consider reaching out immediately:\n\n"
    "🇮🇳 **India** — KIRAN Mental Health Helpline: **1800-599-0019** (24/7, toll-free)\n"
    "🇮🇳 iCall (TISS): **9152987821** (Mon-Sat, 10am-8pm)\n"
    "🌍 If you are outside India, please search for a local crisis helpline or go to your "
    "nearest emergency room.\n\n"
    "If you are in immediate danger, please call your local emergency number right now."
)

_PATTERNS = [
    (["stress", "stressed", "overwhelmed"],
     ["It sounds like you're carrying a lot right now. Want to try a quick breathing "
       "exercise from the Games section, or talk about what's weighing on you?",
      "Feeling overwhelmed is exhausting. What's the biggest thing on your mind at the moment?"]),
    (["anxious", "anxiety", "nervous", "worried"],
     ["Anxiety can be really uncomfortable. Try grounding yourself: name 3 things you can see "
       "right now. Do you want to talk about what's triggering it?",
      "That sounds tough. Sometimes slow breathing helps in the moment — there's a guided "
       "breathing exercise in the Anti-Stress Games tab if you'd like to try it."]),
    (["sad", "down", "unhappy", "depressed", "low"],
     ["I'm sorry you're feeling low. You don't have to carry it alone — do you want to write "
       "about it in the Mood Tracker so we can keep an eye on the pattern?",
      "That sounds heavy. Is there something specific that happened, or is it more of a general feeling?"]),
    (["tired", "exhausted", "burnt out", "burnout"],
     ["Rest is productive too. Have you been able to get proper sleep lately?",
      "Burnout is real. Even a 5-minute break with one of the anti-stress games might help reset a little."]),
    (["happy", "good", "great", "excited"],
     ["That's wonderful to hear! What's been going well for you?",
      "Love that energy — want to log it in the Mood Tracker so future-you can look back on it?"]),
    (["lonely", "alone", "isolated"],
     ["Feeling lonely is genuinely hard. Is there someone you trust you could reach out to today, "
       "even just a short message?",
      "You're not alone in this conversation, at least. What's been making you feel isolated lately?"]),
    (["thanks", "thank you", "thx"],
     ["Anytime. Take care of yourself 💙", "Glad I could help a little. I'm here whenever you need."]),
    (["hi", "hello", "hey"],
     ["Hey there 👋 I'm MindMate. How are you feeling today?",
      "Hi! I'm here to listen. What's on your mind?"]),
]

_FALLBACK = [
    "Thanks for sharing that. Can you tell me a bit more about how that's making you feel?",
    "I hear you. What do you think would help right now, even a little?",
    "That sounds important. Want to log this in the Mood Tracker so we can track how you're doing over time?",
]


def is_crisis_message(text: str) -> bool:
    lowered = text.lower()
    return any(kw in lowered for kw in CRISIS_KEYWORDS)


def get_bot_response(text: str) -> str:
    if is_crisis_message(text):
        return CRISIS_RESPONSE

    lowered = text.lower()
    for keywords, responses in _PATTERNS:
        if any(kw in lowered for kw in keywords):
            return random.choice(responses)

    return random.choice(_FALLBACK)
