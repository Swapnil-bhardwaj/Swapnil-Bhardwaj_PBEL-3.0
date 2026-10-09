"""
chatbot_logic.py
-----------------
MindMate Campus Peer Buddy logic.
Empathetic, authentic rule-based conversational assistant designed specifically
around student challenges: exam pressure, all-nighters, group projects,
imposter syndrome, and academic burnout.

Zero corporate jargon, zero clinical stiffness -- speaks like a caring,
thoughtful college peer or mentor.
"""

from __future__ import annotations
import random

CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "self harm", "self-harm",
    "hurt myself", "want to die", "no reason to live", "can't go on",
]

CRISIS_RESPONSE = (
    "💙 **I hear how much pain you're in, and you don't have to carry this alone.**\n\n"
    "Your life and wellbeing matter infinitely more than any exam, college pressure, or situation. "
    "Please talk to someone who can truly support you right now:\n\n"
    "🇮🇳 **KIRAN Mental Health Helpline (India):** [1800-599-0019](tel:18005990019) (24/7, Toll-Free)\n"
    "🇮🇳 **iCall (TISS):** [9152987821](tel:9152987821) (Mon–Sat, 10am–8pm)\n"
    "🇮🇳 **Tele-MANAS:** [14416](tel:14416) or [1800-891-4416](tel:18008914416) (24/7 National)\n"
    "🌍 **Outside India:** Please reach out to your local university student counseling center or emergency health services.\n\n"
    "Please reach out to a trusted friend, family member, or counselor right away."
)

_PATTERNS = [
    # Exams & Tests
    (["exam", "exams", "test", "viva", "midterm", "finals", "marks", "grade", "gpa"],
     ["The pre-exam dread is so intense, but remember: an exam score is just feedback on a piece of paper. It does not measure your intelligence, your worth, or your future. Have you taken a 15-minute breather away from your notes today?",
      "Exams make everything feel life-or-death, but you've passed through dozens of stressful tests before this. What specific topic or chapter is making you feel stuck right now?",
      "Take a deep breath. Focus on mastering just one concept or problem right now instead of worrying about the entire syllabus."]),

    # Assignments & Submissions
    (["assignment", "submission", "deadline", "project", "homework", "lab report"],
     ["Submission season is brutal. If the assignment feels like an intimidating mountain, try the 'bad first draft' trick—just write out messy notes without editing. A rough draft can always be fixed; a blank page just breeds anxiety.",
      "Deadlines piling up? Prioritize ruthlessly: what is strictly due in the next 24 hours? Focus solely on that one deliverable and put the rest out of your mind for now."]),

    # Procrastination & Focus
    (["procrastinat", "distract", "can't focus", "cannot focus", "unproductive", "wasting time"],
     ["Procrastination usually isn't laziness—it's emotional overwhelm. When a task feels huge or stressful, our brain naturally seeks quick relief. Try the 5-Minute Rule: sit down and commit to working on the task for just 5 minutes. If you want to stop after 5 mins, you can.",
      "We've all been trapped in the doom-scrolling loop before deadlines. Try changing your physical spot: move from your bed to a desk, or head to the campus library. Also, check out the Lo-Fi soundscapes in our Games tab!"]),

    # Sleep & All-Nighters
    (["all-nighter", "sleep", "insomnia", "tired", "exhausted", "sleepless", "3 am", "4 am"],
     ["Pulling an all-nighter cuts your memory consolidation by more than half. If you're running on empty, even a 90-minute sleep cycle or 20-minute power nap will recharge your brain far better than staring blindly at slides.",
      "Your brain is crying out for rest! Grab a glass of water, step away from bright blue screens, and give yourself permission to sleep. You'll think so much clearer tomorrow morning."]),

    # Burnout & Overwhelmed
    (["burnout", "burnt out", "overwhelmed", "crying", "breaking down", "too much"],
     ["Let's pause right here. Drop your shoulders down from your ears, unclench your jaw, and take one deep slow breath. You've been running on overdrive for too long. What can you take off your plate for just tonight?",
      "Academic burnout is your mind telling you it's running on empty fumes. Pushing harder won't fix it—rest will. Even 20 minutes doing something completely non-academic helps reset your system."]),

    # Group Projects & Team Friction
    (["group project", "teammate", "team member", "partner", "group work"],
     ["Group projects can test anyone's sanity. It's so frustrating when you feel like you're carrying the entire workload. Have you clearly divided specific bullet points with deadlines in the group chat, or is everyone waiting on each other?",
      "Group project friction is an unfortunate campus rite of passage. Protect your peace: document your work clearly, stay civil, and focus on delivering your part exceptionally."]),

    # Career, Internships & Imposter Syndrome
    (["internship", "placement", "job", "career", "resume", "cv", "interview", "imposter"],
     ["Seeing everyone's shiny LinkedIn announcements can trigger severe imposter syndrome. Keep in mind: people only post their highlight reels, never their 50 rejections. You are on your own timeline.",
      "Career anxiety is so heavy in college, but you don't need your whole life sorted out this semester. What's one small, concrete step you can take today—like reaching out to an alum or tweaking one project description?"]),

    # Hostel Life, Mess Food & Homesickness
    (["hostel", "mess food", "roommate", "homesick", "missing home"],
     ["Hostel life can feel isolating, especially when the food is bad and you're missing home cooking. Have you had a chance to call home or catch up with an old school friend today? Even a 10-minute chat works wonders.",
      "Living in student dorms or hostels has zero privacy and lots of noise. If you're feeling drained, try slipping away to a quiet corner on campus, put on headphones, and recharge your social battery."]),

    # Anxiety & Stress
    (["stress", "stressed", "anxious", "anxiety", "nervous", "panic"],
     ["Anxiety loves making things feel urgent and catastrophic. Let's ground ourselves: name 3 physical objects around you, and take a slow box breath (check the breathing orb in the Games tab!).",
      "I'm right here with you. What feels like the heaviest weight right now? Let's untangle it together."]),

    # Loneliness
    (["lonely", "alone", "isolated", "no friends"],
     ["College can paradoxically be one of the loneliest places, even surrounded by hundreds of peers. Feeling disconnected is so common, even if nobody talks about it. Is there a campus club, library study session, or casual hobby group you might peek into?",
      "You are not alone right now. I'm here to listen without judgment. Tell me what's been on your mind lately."]),

    # Happiness & Wins
    (["happy", "proud", "passed", "scored", "nailed", "good", "great", "relieved"],
     ["YES! That is such a huge win! 🎉 Make sure you take a moment to celebrate and treat yourself (chai, favorite food, or chilling with friends). You earned this!",
      "Love to see that energy! Savor this feeling and drop a quick note in the Mood Journal so future-you can look back at this victory."]),

    # Gratitude & Chit-Chat
    (["thanks", "thank you", "thx", "appreciate"],
     ["Anytime, friend! Always in your corner. Take care of yourself today 💙",
      "Always here whenever you need to vent or reset. Go crush your day!"]),

    (["hi", "hello", "hey", "sup", "yo"],
     ["Hey! 👋 How is the college hustle treating you today?",
      "Hey there! Ready to listen. Did classes go okay today, or is something stressing you out?"]),
]

_FALLBACK = [
    "I hear you. College life can throw so much at you all at once. What do you feel would help bring a little bit of relief right now?",
    "That sounds tough to carry alone. Do you want to unpack that a bit more, or would taking a 5-minute breather with a mini-game help reset your mind?",
    "Thanks for sharing that with me. Remember to be kind to yourself today—you're doing the best you can with a demanding schedule.",
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
