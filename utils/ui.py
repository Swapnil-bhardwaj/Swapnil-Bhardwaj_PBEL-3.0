"""
ui.py
-----
Shared styling, student theme helpers, and UI components for MindMate.
Provides a modern, warm, student-focused aesthetic that feels handcrafted
and personal rather than generic or robotic.
"""

import streamlit as st
import random

STUDENT_AFFIRMATIONS = [
    "Your worth is not defined by your GPA or a single exam score. 💙",
    "Resting is part of studying. Your brain needs downtime to consolidate memories. 🧠",
    "One assignment at a time. You don't have to solve your whole future today. ☕",
    "It's completely okay to take a break without feeling guilty. 🌿",
    "Progress isn't linear. Submitting something good enough beats not submitting at all. ✨",
    "You've survived 100% of your hardest semester deadlines so far. You've got this. 🚀",
    "Drink some water, unclench your jaw, and let your shoulders drop. 💧",
    "Comparison is a joy-thief. Everyone's running their own unique marathon. 🏃",
]

CAMPUS_TIPS = [
    ("👀 20-20-20 Rule", "Every 20 mins of staring at slides/screens, look at an object 20 feet away for 20 seconds."),
    ("💧 Hydration Check", "Keep a water bottle on your study desk. Mild dehydration drops focus by up to 15%."),
    ("🚶 5-Min Walk Reset", "Stuck on a tricky problem or bug? A quick walk around the hostel or campus unclogs mental blocks."),
    ("🌙 Sleep > All-Nighters", "Pulling an all-nighter cuts cognitive retention drastically. 6 hours of sleep beats cramming all night."),
]


def apply_student_theme():
    """Injects custom CSS to give the app a clean, modern, student-crafted look."""
    custom_css = """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@400;500;600;700&display=swap');

    /* Global Typography & Backgrounds */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    h1, h2, h3, h4 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    /* Streamlit Main Container Spacing */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1100px !important;
    }

    /* Student Badge Pill */
    .student-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, #EEF2FF, #E0E7FF);
        color: #4338CA;
        font-weight: 600;
        font-size: 0.82rem;
        padding: 5px 14px;
        border-radius: 9999px;
        border: 1px solid #C7D2FE;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(99, 102, 241, 0.08);
    }

    /* Student Card Component */
    .student-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 18px -2px rgba(15, 23, 42, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }
    .student-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px -4px rgba(99, 102, 241, 0.12);
        border-color: #CBD5E1;
    }

    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #A855F7 100%);
        color: white;
        padding: 2.2rem 2.4rem;
        border-radius: 22px;
        margin-bottom: 1.8rem;
        box-shadow: 0 12px 32px -4px rgba(79, 70, 229, 0.3);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::after {
        content: "";
        position: absolute;
        top: -40px;
        right: -40px;
        width: 180px;
        height: 180px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        pointer-events: none;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
        color: white !important;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        opacity: 0.92;
        line-height: 1.5;
        max-width: 650px;
        color: #F1F5F9;
    }

    /* Daily Affirmation Pill */
    .affirmation-box {
        background: linear-gradient(135deg, #FEF3C7, #FDE68A);
        border: 1px solid #FCD34D;
        color: #92400E;
        padding: 0.9rem 1.3rem;
        border-radius: 14px;
        font-weight: 600;
        font-size: 0.94rem;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1.5rem;
    }

    /* Feature Grid Nav Cards */
    .nav-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 1.3rem;
        text-decoration: none;
        color: inherit;
        display: block;
        height: 100%;
        transition: all 0.22s ease-in-out;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
    }
    .nav-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.15);
        border-color: #A5B4FC;
    }
    .nav-icon {
        font-size: 2rem;
        margin-bottom: 0.6rem;
    }
    .nav-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.3rem;
    }
    .nav-desc {
        font-size: 0.88rem;
        color: #64748B;
        line-height: 1.45;
    }

    /* Modern Metric Card */
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 1rem 1.2rem;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.03);
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        color: #4F46E5 !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 0.55rem 1.3rem !important;
        transition: all 0.2s ease !important;
        border: 1px solid transparent !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2) !important;
    }

    /* Form Inputs */
    .stTextArea textarea {
        border-radius: 14px !important;
        border: 1px solid #CBD5E1 !important;
        padding: 12px 14px !important;
        font-size: 0.95rem !important;
    }
    .stTextArea textarea:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
    }

    /* Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F1F5F9;
        padding: 6px;
        border-radius: 14px;
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 18px;
        font-weight: 600;
        font-size: 0.92rem;
        color: #475569;
        border: none !important;
        background: transparent;
    }
    .stTabs [aria-selected="true"] {
        background: #FFFFFF !important;
        color: #4F46E5 !important;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08);
    }

    /* Sidebar Tweaks */
    [data-testid="stSidebar"] {
        background: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }

    /* Student Footer */
    .student-footer {
        text-align: center;
        padding: 2rem 1rem 1rem;
        color: #94A3B8;
        font-size: 0.85rem;
        border-top: 1px solid #E2E8F0;
        margin-top: 2.5rem;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


def render_student_header(title: str, subtitle: str, badge: str = "🎓 Student Wellness"):
    """Renders a clean, cohesive header for subpages."""
    st.markdown(
        f"""
        <div style="margin-bottom: 1.6rem;">
            <div class="student-badge">✨ {badge}</div>
            <h1 style="font-size: 2.1rem; color: #1E293B; margin-bottom: 0.3rem;">{title}</h1>
            <p style="color: #64748B; font-size: 1.02rem; margin: 0; line-height: 1.5;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_random_affirmation():
    """Displays a supportive, authentic affirmation for students."""
    quote = random.choice(STUDENT_AFFIRMATIONS)
    st.markdown(
        f"""
        <div class="affirmation-box">
            <span style="font-size: 1.3rem;">💡</span>
            <span><strong>Friendly Reminder:</strong> {quote}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_campus_tip_card():
    """Renders a random quick campus survival tip."""
    title, desc = random.choice(CAMPUS_TIPS)
    st.markdown(
        f"""
        <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 14px; padding: 1rem 1.2rem; margin-top: 0.8rem;">
            <div style="font-weight: 700; color: #166534; font-size: 0.95rem; margin-bottom: 4px;">{title}</div>
            <div style="color: #15803D; font-size: 0.88rem; line-height: 1.4;">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    """Renders a warm, personal student footer."""
    st.markdown(
        """
        <div class="student-footer">
            <strong>MindMate</strong> • Built by students, for students 🎒<br>
            All journals and quiz answers are stored 100% locally on your machine — zero cloud tracking.
        </div>
        """,
        unsafe_allow_html=True,
    )
