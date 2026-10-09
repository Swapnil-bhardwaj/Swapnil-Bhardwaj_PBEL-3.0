"""
app.py
------
MindMate | Campus Wellness & Student Calm Companion
Entry point for the application.
"""

import streamlit as st
from utils.storage import load_mood_log, clear_all_data
from utils.ui import apply_student_theme, render_random_affirmation, render_campus_tip_card, render_footer

st.set_page_config(
    page_title="MindMate | Student Wellness Hub",
    page_icon="🎓",
    layout="wide",
)

# Apply cohesive student aesthetic
apply_student_theme()

# Top Hero Section
st.markdown(
    """
    <div class="hero-banner">
        <div style="display: inline-block; background: rgba(255, 255, 255, 0.2); padding: 4px 14px; border-radius: 999px; font-size: 0.82rem; font-weight: 600; margin-bottom: 0.8rem; letter-spacing: 0.03em;">
            🎒 CAMPUS WELLNESS SANCTUARY
        </div>
        <div class="hero-title">MindMate 🎓</div>
        <div class="hero-subtitle">
            A private, judgment-free space built by students, for students. Untangle exam anxiety, track your daily vibes, and recharge between study sessions.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Daily supportive affirmation
render_random_affirmation()

# Notice banner styled gently
st.info(
    "💡 **Friendly Note:** MindMate is a peer-oriented self-awareness tool for everyday campus life and study stress. "
    "It is not a clinical medical service. If you are ever feeling overwhelmed or in crisis, please check the helpline numbers in the **MindMate Buddy** page.",
    icon="💙",
)

st.markdown("<h3 style='margin-top: 1.2rem; margin-bottom: 0.8rem;'>🚀 Quick Student Toolkit</h3>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="student-card">
            <div style="font-size: 2.2rem; margin-bottom: 6px;">📝</div>
            <div style="font-weight: 700; font-size: 1.1rem; color: #1E293B; margin-bottom: 4px;">Mood Journal</div>
            <div style="font-size: 0.86rem; color: #64748B; line-height: 1.45; min-height: 52px;">
                Vent about tough classes, group project drama, or wins. Get instant sentiment reflection.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/1_Mood_Tracker.py", label="Open Mood Journal ➔", icon="📝")

with col2:
    st.markdown(
        """
        <div class="student-card">
            <div style="font-size: 2.2rem; margin-bottom: 6px;">📊</div>
            <div style="font-weight: 700; font-size: 1.1rem; color: #1E293B; margin-bottom: 4px;">Stress Check-In</div>
            <div style="font-size: 0.86rem; color: #64748B; line-height: 1.45; min-height: 52px;">
                A 10-question pulse check tailored for academic pressure, all-nighters, and burnout.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/2_Stress_Quiz.py", label="Take Stress Check ➔", icon="📊")

with col3:
    st.markdown(
        """
        <div class="student-card">
            <div style="font-size: 2.2rem; margin-bottom: 6px;">💬</div>
            <div style="font-weight: 700; font-size: 1.1rem; color: #1E293B; margin-bottom: 4px;">Peer Chat Buddy</div>
            <div style="font-size: 0.86rem; color: #64748B; line-height: 1.45; min-height: 52px;">
                A warm, listening companion who understands exam dread, late nights, and imposter syndrome.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/3_Chatbot.py", label="Chat with Buddy ➔", icon="💬")

with col4:
    st.markdown(
        """
        <div class="student-card">
            <div style="font-size: 2.2rem; margin-bottom: 6px;">🎮</div>
            <div style="font-weight: 700; font-size: 1.1rem; color: #1E293B; margin-bottom: 4px;">Study Break Hub</div>
            <div style="font-size: 0.86rem; color: #64748B; line-height: 1.45; min-height: 52px;">
                8 anti-stress games: study soundscapes, bubble pop, zen sand garden, ripple pond, & more.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/4_Anti_Stress_Games.py", label="Play & Unwind ➔", icon="🎮")

st.markdown("<hr style='margin: 2rem 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

# Mood History & Analytics Section
left_col, right_col = st.columns([1.6, 1])

with left_col:
    st.markdown("<h3 style='margin-bottom: 0.6rem;'>📈 Your Recent Vibe Trend</h3>", unsafe_allow_html=True)
    df = load_mood_log()
    if df.empty:
        st.markdown(
            """
            <div style="background: white; border: 1px dashed #CBD5E1; border-radius: 16px; padding: 2rem; text-align: center; color: #64748B;">
                <div style="font-size: 2rem; margin-bottom: 8px;">📓</div>
                <strong>Your journal is currently empty.</strong><br>
                Drop your first journal entry in the <a href="pages/1_Mood_Tracker.py" style="color: #4F46E5; font-weight: 600;">Mood Journal</a> to start tracking your semester emotional curve!
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        recent = df.tail(7)
        m1, m2, m3 = st.columns(3)
        m1.metric("Journals Logged", f"{len(df)} 📝")
        m2.metric("Latest Feeling", f"{recent.iloc[-1]['mood_label']}")
        avg_pol = recent['polarity'].mean()
        vibe_str = "Positive" if avg_pol > 0.1 else ("Needs TLC" if avg_pol < -0.1 else "Balanced")
        m3.metric("7-Day Vibe", f"{avg_pol:+.2f} ({vibe_str})")

        st.line_chart(df.set_index("timestamp")["polarity"], height=220)

with right_col:
    st.markdown("<h3 style='margin-bottom: 0.6rem;'>💡 Campus Tip of the Day</h3>", unsafe_allow_html=True)
    render_campus_tip_card()
    
    st.markdown(
        """
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px; padding: 1.2rem; margin-top: 1rem;">
            <div style="font-weight: 700; color: #1E293B; margin-bottom: 6px;">☕ Need a 2-Minute Reset?</div>
            <ul style="font-size: 0.88rem; color: #475569; padding-left: 1.2rem; margin-bottom: 0; line-height: 1.6;">
                <li>Unclench your jaw and let your shoulders drop.</li>
                <li>Take 3 deep box breaths in the games tab.</li>
                <li>Drink a glass of water before returning to your notes.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr style='margin: 2rem 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

with st.expander("🔒 Student Privacy & Data Control"):
    st.markdown(
        """
        We take student privacy seriously. Your journal entries, feelings, and quiz responses are stored 
        **100% locally** on your machine in the `data/` folder as simple CSV files.
        - **No cloud telemetry**
        - **No accounts or logins**
        - **Your thoughts stay strictly on your laptop**
        """
    )
    if st.button("🗑️ Clear Local History & Reset Data", type="secondary"):
        clear_all_data()
        st.success("All local entries and quiz logs have been wiped clean.")
        st.rerun()

render_footer()
