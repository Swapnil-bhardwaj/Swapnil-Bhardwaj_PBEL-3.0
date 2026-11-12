"""
chatbot_logic.py
-----------------
MindMate Campus Peer Buddy - Intelligent & Polite Conversational Dialogue Engine.

Designed specifically to speak politely, warmly, and constructively with students.
Integrates:
1. Empathetic, respectful, and courteous conversational manners.
2. Sentiment analysis via TextBlob to dynamically mirror emotional state with care.
3. Multi-turn context memory & topic tracking (handles follow-ups, examples, questions).
4. Extensive student knowledge base (study techniques, exam anxiety, time management,
   group projects, sleep hygiene, mindfulness, and gentle motivation).
5. Optional Generative AI fallback (via Google Gemini REST API) if an API key is provided,
   while running 100% offline and rich by default.
6. Immediate, gentle crisis detection with helpline support.
"""

from __future__ import annotations
import random
import re
import time
from typing import Generator, List, Dict, Tuple, Optional
from textblob import TextBlob
import requests

# Crisis keywords that warrant immediate compassionate helpline guidance
CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "self harm", "self-harm",
    "hurt myself", "want to die", "no reason to live", "can't go on",
    "ending it all", "give up on life",
]

CRISIS_RESPONSE = (
    "💙 **Please know that you are not alone, and your life and wellbeing matter deeply.**\n\n"
    "I can hear how much pain you are experiencing right now. Please treat yourself with kindness and reach out to someone who can provide immediate, compassionate support:\n\n"
    "🇮🇳 **Tele-MANAS (Govt of India):** [14416](tel:14416) or [1800-891-4416](tel:18008914416) *(24/7, Toll-Free)*\n"
    "🇮🇳 **KIRAN Mental Health Helpline:** [1800-599-0019](tel:18005990019) *(24/7, Toll-Free)*\n"
    "🇮🇳 **iCall (TISS):** [9152987821](tel:9152987821) *(Mon–Sat, 10:00 AM – 8:00 PM)*\n"
    "🎓 **Campus Counseling:** Please consider contacting your university student wellness center or hostel warden.\n"
    "🌍 **Outside India:** Please reach out to your local emergency helpline or student health services.\n\n"
    "Please consider sharing how you feel with a trusted friend, family member, or counselor right now. You deserve care and support."
)

# Courteous openings & closings based on tone
POLITE_OPENINGS = {
    "Warm & Encouraging": [
        "Thank you so much for sharing that with me.",
        "I truly appreciate you reaching out and opening up.",
        "It is always a pleasure to speak with you.",
        "I completely hear you, and I am glad you brought this up.",
        "I understand how important this is to you.",
    ],
    "Practical & Study-Focused": [
        "Thank you for reaching out. Let's look at this step-by-step together.",
        "I appreciate your question. Here is a clear, structured way we can approach this.",
        "Glad you asked. Let's break this down into practical, actionable steps.",
        "Thank you for bringing this up. Let us organize this effectively for you.",
    ],
    "Calm & Grounding": [
        "Please take a gentle breath. I am right here with you.",
        "Thank you for taking a moment to pause and chat.",
        "Let us slow things down for a moment together.",
        "I hear you softly and clearly. You are safe to take your time.",
    ]
}

POLITE_CLOSINGS = [
    "Does this feel helpful, or would you like to explore another approach together?",
    "Please let me know if you would like me to explain any part in more detail.",
    "How does that sound to you? I am always happy to adjust to what fits you best.",
    "Please take all the time you need. How are you feeling about this right now?",
    "Would you like a concrete example, or shall we talk through your next step?",
]

# Domain-specific knowledge base containing detailed polite explanations
KNOWLEDGE_BASE = [
    {
        "id": "greetings",
        "keywords": ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening", "sup", "yo"],
        "exact_matches": ["hi", "hello", "hey", "hello there", "good morning", "good evening", "good afternoon"],
        "responses": [
            "Hello there! It is truly wonderful to connect with you today. 😊 How are your classes and studies going, and how may I assist you?",
            "Greetings! I am MindMate, your campus companion. Whether you would like study advice, need to vent about a busy week, or just want a friendly conversation, I am delighted to be here with you.",
            "Hello! I hope you are having a pleasant day so far. Please feel free to tell me what is on your mind today.",
        ],
        "follow_up": "Is there a specific topic, assignment, or feeling you would like to talk through?"
    },
    {
        "id": "identity",
        "keywords": ["who are you", "what can you do", "what are you", "your name", "help me with", "capabilities"],
        "responses": [
            "I am **MindMate**, an empathetic companion built specifically to support students like you! 🎓\n\nHere is how I can politely and practically assist you:\n- **Study & Focus Strategies:** Techniques like Pomodoro, Active Recall, and the Feynman method.\n- **Exam & Deadline Support:** Coping with test anxiety, handling stressful submissions, and overcoming procrastination.\n- **Mindfulness & Grounding:** Guided box breathing, 5-4-3-2-1 grounding, and anti-burnout check-ins.\n- **College Life & Peer Advice:** Navigating group project friction, hostel adjustments, and imposter syndrome.\n\nPlease feel free to ask me anything or share how your day is going!",
        ],
        "follow_up": "Would you like to try a study technique, talk about an upcoming exam, or take a quick relaxation break?"
    },
    {
        "id": "how_are_you",
        "keywords": ["how are you", "how are you doing", "how do you do", "how is it going"],
        "responses": [
            "Thank you so much for your kind inquiry! I am doing very well, and it brings me great joy to be here chatting with you. 😊 More importantly, how are you feeling today?",
            "I am doing wonderfully, thank you for asking so politely! How has your day treated you so far? I would love to hear about it.",
        ],
        "follow_up": "How has your academic week been treating you so far?"
    },
    {
        "id": "study_techniques",
        "keywords": ["study technique", "how to study", "best way to study", "study method", "learn faster", "memorize", "study tip", "study tips"],
        "responses": [
            "I would be delighted to share some evidence-based study techniques that work exceptionally well for university students:\n\n1. **The Feynman Technique:** Try explaining the concept out loud in plain, simple terms as if teaching a beginner. If you get stuck on jargon, you've pinpointed exactly what to review.\n2. **Active Recall & Spaced Repetition:** Instead of passively rereading slides, close your notebook and write down everything you remember (the *blurting method*), or use flashcards with spaced review intervals.\n3. **The Pomodoro System:** Study with deep focus for 25 or 50 minutes, followed by a strict 5- or 10-minute break away from screens.\n4. **Cornell Note-Taking:** Divide your page into *Notes*, *Cues/Keywords*, and a brief 2-sentence *Summary* at the bottom for effortless revision.",
        ],
        "follow_up": "Would you like me to elaborate on one of these specific techniques, like the Feynman method or Active Recall?"
    },
    {
        "id": "pomodoro",
        "keywords": ["pomodoro", "25 minutes", "timer technique", "study timer"],
        "responses": [
            "The **Pomodoro Technique** is one of the most effective and gentle productivity methods for students! Here is the polite and practical way to apply it:\n\n1. **Select One Task:** Choose one single assignment, chapter, or problem set.\n2. **Set a Timer for 25 Minutes:** During this block (one *Pomodoro*), put your phone on 'Do Not Disturb' and work solely on this item.\n3. **Take a 5-Minute Pure Break:** Step away from your desk, stretch, grab water, or look out a window.\n4. **After 4 Pomodoros:** Take a longer, rewarding break of 20 to 30 minutes.\n\n*Pro-tip:* If 25 minutes feels too short for technical subjects like coding or math, try the **50/10 rhythm** (50 mins focus, 10 mins break).",
        ],
        "follow_up": "Would you like to try starting one Pomodoro session today?"
    },
    {
        "id": "active_recall",
        "keywords": ["active recall", "spaced repetition", "flashcard", "anki", "blurting"],
        "responses": [
            "**Active Recall** is scientifically proven to be significantly more effective than passive highlighting or rereading.\n\nHere is how you can use it right away:\n- **The Blurting Method:** Read a subtopic for 10 minutes. Close the book, take a blank sheet of paper, and write or draw everything you can recall from memory. Compare with your notes to spot gaps.\n- **Self-Testing:** Turn your lecture slide headings into questions. For instance, turn *'Types of Sorting Algorithms'* into *'What are the key trade-offs between QuickSort and MergeSort?'*\n- **Spaced Repetition:** Review the newly learned material after 1 day, then 3 days, then 7 days to permanently solidify it into long-term memory.",
        ],
        "follow_up": "What subject or topic are you currently studying where we could apply this?"
    },
    {
        "id": "feynman",
        "keywords": ["feynman", "feynman technique", "explain simply"],
        "responses": [
            "The **Feynman Technique** is named after Nobel prize-winning physicist Richard Feynman and is designed to turn complex ideas into crystal-clear understanding:\n\n1. **Choose Your Concept:** Write the title at the top of a blank page.\n2. **Explain it to a 12-Year-Old:** Use plain language without technical jargon or buzzwords.\n3. **Identify Knowledge Holes:** Whenever you find yourself using vague phrases or struggling to explain a connection, return to your textbook to clarify it.\n4. **Simplify and Create an Analogy:** Connect the idea to everyday real-world phenomena.",
        ],
        "follow_up": "Is there a tricky concept you are grappling with right now that we could break down together?"
    },
    {
        "id": "exams",
        "keywords": ["exam", "exams", "test", "tests", "midterm", "midterms", "finals", "viva", "paper", "quiz"],
        "responses": [
            "I completely understand how heavy exam pressure can feel. Please remember that **an exam score measures your recall on one given day, not your intellect, character, or future potential.**\n\nHere are gentle, constructive strategies to navigate exam season:\n- **Triage the Syllabus:** Categorize topics into *High Yield / Confident*, *Moderate / Needs Practice*, and *Critical Gaps*. Spend 70% of your energy on high-weightage topics you can master.\n- **Practice Past Papers:** Solving previous question papers under timed conditions reduces exam-day panic more effectively than rereading notes.\n- **Protect Your Sleep:** Your brain processes memory consolidation during deep sleep. A rested mind with 80% preparation will score higher than an exhausted mind with 100% preparation.",
        ],
        "follow_up": "When is your next exam, and what subject is it on?"
    },
    {
        "id": "procrastination",
        "keywords": ["procrastinat", "procrastinating", "procrastination", "can't start", "delaying", "putting off", "distracted", "doomscroll"],
        "responses": [
            "First of all, please be gentle with yourself. **Procrastination is rarely laziness—it is usually an emotional response to overwhelm or fear of not doing it perfectly.**\n\nHere is a polite, proven way to gently break the freeze:\n- **The 5-Minute Rule:** Make a gentle agreement with yourself: *'I will only work on this for five minutes. If I still want to stop after five minutes, I am permitted to stop.'* Usually, getting past the initial inertia is 90% of the battle.\n- **Lower the Bar on the First Draft:** Give yourself permission to write a rough, imperfect outline. You can always refine bad notes, but you cannot edit a blank page.\n- **Change Your Physical Environment:** Move from your bed to a desk, or head to the campus library.",
        ],
        "follow_up": "What is the single smallest action you could take on this task right now?"
    },
    {
        "id": "all_nighter",
        "keywords": ["all-nighter", "all nighter", "stayed up all night", "pulled an all nighter", "haven't slept", "no sleep", "3 am", "4 am"],
        "responses": [
            "I truly empathize with the intense academic crunch that leads to pulling all-nighters, but please let me gently remind you of what science tells us:\n\n- Pulling an all-nighter reduces cognitive retention, logic, and short-term working memory by up to **50%**.\n- If you have an exam or submission tomorrow, getting even **90 minutes** (one complete REM cycle) or a **20-minute power nap** will significantly restore your alertness.\n- Please drink a tall glass of room-temperature water, unclench your jaw, and give yourself permission to close your eyes. Your mind deserves restorative rest.",
        ],
        "follow_up": "Can you take a short 20 to 30-minute power nap right now to recharge?"
    },
    {
        "id": "burnout",
        "keywords": ["burnout", "burnt out", "exhausted", "drained", "overwhelmed", "breaking down", "too much work", "can't keep up"],
        "responses": [
            "Please take a deep, slow breath and let your shoulders drop down away from your ears. **Academic burnout is not a sign of weakness—it is your nervous system letting you know that you have been operating at maximum capacity for too long without replenishing your reserves.**\n\nHere are three compassionate steps you can take today:\n1. **Ruthlessly Drop the Non-Essentials:** Ask yourself: *'What happens if I don't do this today?'* If the world doesn't collapse, postpone it.\n2. **A Complete Cognitive Disconnect:** Step away from laptop and phone screens for 30 minutes. Go for a gentle walk or listen to our Lo-Fi Soundscapes in the Anti-Stress Games tab.\n3. **Remember Your Baseline:** You are a human being going to college, not a machine. Taking rest is a productive necessity, not an indulgence.",
        ],
        "follow_up": "What is one non-urgent responsibility you could safely take off your plate this evening?"
    },
    {
        "id": "group_projects",
        "keywords": ["group project", "teammate", "team member", "group work", "freeloader", "not doing work", "partner isn't helping"],
        "responses": [
            "Group project difficulties can test anyone's patience! It is deeply frustrating when you feel like you are shouldering the burden while others are disengaged.\n\nHere is a professional, polite way to manage it:\n1. **Document Clearly in Writing:** In your group chat or shared document, create a clean checklist: `[Task] -> [Assigned Name] -> [Agreed Deadline]`.\n2. **Establish a Check-in Date:** Say politely: *'Hey everyone, let's aim to have our first drafts merged by Thursday so we have time to review together.'*\n3. **Protect Your Contribution:** Keep your commits and contributions well-documented in git or document version history.\n4. **Escalate Professionally If Needed:** If a member remains completely unresponsive, politely inform your professor: *'We wanted to ask for your guidance on how to best distribute remaining deliverables given current project participation.'*",
        ],
        "follow_up": "What is the next upcoming milestone for this group project?"
    },
    {
        "id": "imposter_syndrome",
        "keywords": ["imposter", "imposter syndrome", "not good enough", "everyone is smarter", "behind everyone", "falling behind", "failure", "i failed", "low marks"],
        "responses": [
            "Please hear me on this: **You belong here just as much as anyone else in your classroom.**\n\nImposter syndrome is extraordinarily common in university environments because people only broadcast their victories and shiny LinkedIn announcements, never their fifty rejections, anxiety, or late-night doubts.\n\n- **Compare Yourself Only to Past You:** Think about how much you know today compared to two years ago. That growth is real.\n- **A Bad Grade is Data, Not a Verdict:** A poor score simply tells you *'this specific concept needs a different approach'*; it has zero bearing on your worth or intellect.\n- **Adopt a Growth Mindset:** Struggle is the exact physiological sensation of your brain forming new neural connections.",
        ],
        "follow_up": "Would you like to reflect on one skill or subject you've improved at since starting college?"
    },
    {
        "id": "time_management",
        "keywords": ["time management", "schedule", "routine", "organize my day", "manage time", "not enough time"],
        "responses": [
            "Effective time management for students isn't about packing every minute with study—it's about creating **predictable blocks for deep work so you can enjoy guilt-free rest**.\n\nHere is a simple, proven framework:\n1. **The 'Rule of 3':** Every morning, write down the 3 most important tasks you must accomplish today. Focus on those before anything else.\n2. **Time-Blocking:** Dedicate specific hours to specific subjects (e.g., 2:00 PM – 4:00 PM: Data Structures lab; 4:30 PM – 5:30 PM: Gym or walk).\n3. **Buffer Time:** Always budget 25% extra time for unexpected bugs, complex questions, or sudden meetings.",
        ],
        "follow_up": "Would you like assistance prioritizing your top 3 tasks for tomorrow?"
    },
    {
        "id": "grounding_mindfulness",
        "keywords": ["grounding", "breathe", "breathing", "anxious", "panic", "calm down", "heart racing", "nervous"],
        "responses": [
            "Let's practice the **5-4-3-2-1 Sensory Grounding Technique** right now together. It physically interrupts the stress response in your nervous system:\n\n- Look around and gently name **5 things you can see**.\n- Acknowledge **4 things you can physically touch or feel** (e.g., your desk, your sweater, your feet on the floor).\n- Notice **3 distinct sounds you can hear** right now.\n- Identify **2 things you can smell** around you.\n- Note **1 positive thing about yourself**.\n\nTake one slow, deep breath in through your nose... and a gentle, long exhale through your mouth.",
        ],
        "follow_up": "How did that exercise feel for you just now?"
    },
    {
        "id": "jokes_motivation",
        "keywords": ["joke", "make me laugh", "tell me a joke", "motivation", "motivate me", "inspire me", "quote"],
        "responses": [
            "Here is a lighthearted student chuckle for you: 😄\n\n*Why do programmers prefer dark mode?*\n*Because light attracts bugs!*\n\nAnd here is a grounded truth to carry with you today:\n> *'You don't have to be great to start, but you have to start to be great.'*\n\nYou are working hard, making steady progress, and that deserves immense credit.",
            "Here is a smile for your study break: 😊\n\n*Why was the math book always sad?*\n*Because it had too many problems!*\n\nRemember: Every semester presents hurdles, and every semester you find the strength to overcome them. You've got this!",
        ],
        "follow_up": "Would you like another motivational thought or a study strategy?"
    },
    {
        "id": "gratitude",
        "keywords": ["thank you", "thanks", "thx", "appreciate it", "grateful", "you helped"],
        "responses": [
            "You are most welcome! It is truly my absolute pleasure to assist you. 💙 Please know that you are always welcome here whenever you need advice, encouragement, or a quiet space to reflect.",
            "I am genuinely so glad I could be of help to you! Wishing you calmness, focus, and success in everything you tackle today.",
            "Anytime at all! Thank you for your warmth and courtesy. Remember to stay hydrated and take a proper break today!",
        ],
        "follow_up": "Is there anything else I can assist you with before you head back to your day?"
    },
    {
        "id": "farewell",
        "keywords": ["bye", "goodbye", "see you", "good night", "gotta go", "heading to sleep", "talk later"],
        "responses": [
            "Goodbye for now! Thank you for spending time chatting with me. Have a restful evening or productive day, and I look forward to speaking with you next time! 👋",
            "Take wonderful care of yourself! Get some peaceful rest or enjoy your day, and remember: one step at a time. Until next time! 🌟",
        ],
        "follow_up": ""
    }
]

# Polite general fallback responses when input is open-ended
FALLBACK_RESPONSES = [
    "Thank you for sharing that with me. Academic life presents so many diverse experiences and challenges. May I ask a bit more about what you would like to explore or focus on right now?",
    "I appreciate you bringing that up. I am here to support you in whatever way feels most helpful—whether you would like practical study strategies, emotional reassurance, or a quick study-break reset. Where shall we start?",
    "I hear you clearly, and I value you sharing your thoughts. What would bring you the greatest relief or clarity regarding this right now?",
]

def analyze_sentiment(text: str) -> Tuple[float, float, str]:
    """Computes polarity and subjectivity using TextBlob."""
    try:
        blob = TextBlob(text)
        pol = round(blob.sentiment.polarity, 2)
        subj = round(blob.sentiment.subjectivity, 2)
        if pol <= -0.25:
            mood = "negative"
        elif pol >= 0.25:
            mood = "positive"
        else:
            mood = "neutral"
        return pol, subj, mood
    except Exception:
        return 0.0, 0.0, "neutral"


def detect_topic(text: str) -> Optional[dict]:
    """Matches text against our rich student knowledge base."""
    lowered = text.lower().strip()
    words = set(re.findall(r'\b\w+\b', lowered))
    
    # Check exact matches first (e.g. standalone "hi", "hello")
    for item in KNOWLEDGE_BASE:
        if "exact_matches" in item:
            for em in item["exact_matches"]:
                if lowered == em or lowered.startswith(em + " ") or lowered.endswith(" " + em):
                    return item

    # Match by keywords with scoring
    best_item = None
    best_score = 0
    for item in KNOWLEDGE_BASE:
        score = 0
        for kw in item["keywords"]:
            if " " in kw:
                if kw in lowered:
                    score += 4
            else:
                # Exact word match gets highest weight
                if kw in words:
                    score += 3
                # Prefix matching only for longer stems (>= 4 chars) to avoid false matches like 'yo' -> 'you'
                elif len(kw) >= 4 and any(w.startswith(kw) for w in words):
                    score += 2

        if score > best_score:
            best_score = score
            best_item = item

    if best_score >= 3:
        return best_item
    return None


def handle_context_followup(text: str, history: List[Dict[str, str]]) -> Optional[str]:
    """Handles follow-ups like 'yes', 'tell me more', 'give an example', 'no'."""
    lowered = text.lower().strip()
    
    # Check if there is past conversation
    if not history or len(history) < 2:
        return None
        
    # Get last bot response
    last_bot_msg = ""
    for msg in reversed(history):
        if msg.get("role") == "assistant" or msg.get("sender") == "bot":
            last_bot_msg = msg.get("content", "") or msg.get("text", "")
            break

    # Affirmatives: "yes", "tell me more", "explain more", "sure", "please"
    if any(phrase in lowered for phrase in ["tell me more", "explain more", "more details", "elaborate", "how does that work"]):
        return (
            "I would be glad to elaborate further! In university routines, the key is consistency over perfection. "
            "When you apply this method, start with just one 25-minute study block or one chapter today. "
            "Would you like a step-by-step example of how to schedule it into your afternoon?"
        )
        
    if lowered in ["yes", "yeah", "yep", "sure", "please", "okay", "ok", "definitely"]:
        return (
            "Wonderful! Let's take it one step at a time. First, pick the single most urgent task on your desk right now. "
            "Put your phone across the room or on 'Do Not Disturb', set a 25-minute timer, and begin without worrying about finishing everything. "
            "How does that plan feel for you?"
        )
        
    if lowered in ["no", "nah", "not really", "nope", "i don't think so"]:
        return (
            "I completely respect that! We all have different study styles and rhythms that suit us best. "
            "Would you prefer to talk through how you are feeling, try a quick relaxation exercise, or look at a different subject?"
        )
        
    if "example" in lowered or "give me an example" in lowered:
        return (
            "Certainly! Here is a concrete real-world example:\n\n"
            "Suppose you are studying **Operating Systems (Deadlocks)**:\n"
            "1. *First 20 mins:* Read the 4 conditions for deadlock (Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait).\n"
            "2. *Active Recall:* Close your screen. Draw an analogy on paper (like 4 cars stuck in a 4-way intersection waiting for each other).\n"
            "3. *Self-Testing:* Explain how Bankers Algorithm prevents it in your own words.\n\n"
            "Does that make the approach clearer for your subject?"
        )

    return None


def query_gemini_api(api_key: str, user_prompt: str, history: List[Dict[str, str]], tone: str) -> Optional[str]:
    """Queries Google Gemini REST API if an API key is provided."""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        system_instruction = (
            f"You are MindMate, a polite, respectful, and compassionate campus peer buddy and academic wellness assistant. "
            f"Your tone is {tone}. "
            f"Always address the student with high courtesy, warmth, and respect. "
            f"Provide structured, clear, and actionable advice tailored to college and student life. "
            f"Do not sound robotic or overly clinical; sound like a thoughtful, empathetic senior student or mentor. "
            f"Keep responses concise (2 to 3 paragraphs max) with polite bullet points when helpful, and always close with a polite follow-up question."
        )

        contents = []
        # Add recent conversation turns for context
        for msg in (history or [])[-6:]:
            role = "user" if (msg.get("role") == "user" or msg.get("sender") == "user") else "model"
            text_content = msg.get("content", "") or msg.get("text", "")
            if text_content:
                contents.append({"role": role, "parts": [{"text": text_content}]})
                
        contents.append({"role": "user", "parts": [{"text": user_prompt}]})

        payload = {
            "system_instruction": {"parts": [{"text": system_instruction}]},
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 450,
            }
        }
        headers = {"Content-Type": "application/json"}
        
        res = requests.post(url, json=payload, headers=headers, timeout=12)
        if res.status_code == 200:
            data = res.json()
            candidates = data.get("candidates", [])
            if candidates:
                text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                if text:
                    return text.strip()
    except Exception:
        pass
    return None


def get_bot_response(
    text: str,
    history: Optional[List[Dict[str, str]]] = None,
    tone: str = "Warm & Encouraging",
    api_key: Optional[str] = None
) -> str:
    """
    Main dialogue engine.
    Produces an intelligent, polite, and contextual response.
    """
    cleaned = (text or "").strip()
    if not cleaned:
        return "I am right here with you. Please feel free to type whenever you are ready! 😊"

    lowered = cleaned.lower()

    # 1. Immediate Safety Check
    if any(kw in lowered for kw in CRISIS_KEYWORDS):
        return CRISIS_RESPONSE

    # 2. Check for optional LLM Generative AI API Key
    if api_key and len(api_key.strip()) > 15:
        llm_reply = query_gemini_api(api_key.strip(), cleaned, history or [], tone)
        if llm_reply:
            return llm_reply

    # 3. Contextual Follow-up Check
    followup_reply = handle_context_followup(cleaned, history or [])
    if followup_reply:
        return followup_reply

    # 4. Sentiment Analysis
    polarity, subjectivity, mood = analyze_sentiment(cleaned)

    # 5. Domain Knowledge Matching
    topic_match = detect_topic(cleaned)
    if topic_match:
        core_reply = random.choice(topic_match["responses"])
        follow_up = topic_match.get("follow_up", "")
        
        # Craft polite opening if emotional
        opening = ""
        if mood == "negative" and topic_match["id"] not in ["greetings", "how_are_you", "identity"]:
            opening = f"{random.choice(POLITE_OPENINGS.get(tone, POLITE_OPENINGS['Warm & Encouraging']))}\n\n"
        
        closing = ""
        if follow_up:
            closing = f"\n\n💬 *{follow_up}*"
            
        return f"{opening}{core_reply}{closing}"

    # 6. Sentiment-Guided Polite Conversational Response
    opening = random.choice(POLITE_OPENINGS.get(tone, POLITE_OPENINGS["Warm & Encouraging"]))
    closing = random.choice(POLITE_CLOSINGS)

    if mood == "negative":
        empathetic_msg = (
            f"{opening}\n\n"
            "It sounds like you may be carrying a heavy load right now, and I want to validate that college and daily obligations can genuinely feel overwhelming at times. "
            "Please remember to give yourself grace—you don't have to resolve everything this very minute.\n\n"
            "Would you like to:\n"
            "- Unpack what is weighing on your mind the most?\n"
            "- Break your next task down into manageable 10-minute steps?\n"
            "- Take a 5-minute break with our calming exercises in the **Anti-Stress Games** tab?\n\n"
            f"*{closing}*"
        )
        return empathetic_msg

    if mood == "positive":
        positive_msg = (
            f"{opening}\n\n"
            "It brings me so much happiness to hear your positive energy! 🎉 "
            "Acknowledging and celebrating your wins—both big and small—is a wonderful habit that builds lasting motivation.\n\n"
            "How can we channel this great momentum today? We can dive into a productive study plan or continue celebrating your progress!\n\n"
            f"*{closing}*"
        )
        return positive_msg

    # Neutral fallback with polite guidance
    fallback_core = random.choice(FALLBACK_RESPONSES)
    return f"{opening}\n\n{fallback_core}\n\n*{closing}*"


def stream_response_generator(full_text: str) -> Generator[str, None, None]:
    """Yields words progressively to render a typing animation in Streamlit."""
    words = full_text.split(" ")
    for i, word in enumerate(words):
        yield word + (" " if i < len(words) - 1 else "")
        time.sleep(0.015)
