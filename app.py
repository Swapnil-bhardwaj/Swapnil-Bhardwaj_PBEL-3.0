"""
app.py
------
Entry point for the AI-Based Mental Health Monitoring Solution.

Run with:
    streamlit run app.py

This file only renders the Home / landing page. The other features
(Mood Tracker, Stress Quiz, Chatbot, Anti-Stress Games) live in the
`pages/` folder and are auto-discovered by Streamlit's multipage app
mechanism -- they'll show up in the sidebar automatically.
"""

import streamlit as st
from utils.storage import load_mood_log, clear_all_data

st.set_page_config(
    page_title="MindMate | Mental Health Monitor",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 MindMate — AI-Based Mental Health Monitoring Solution")
st.caption("A student project for tracking mood, assessing stress, and unwinding with anti-stress mini-games.")

st.info(
    "⚠️ **Disclaimer:** MindMate is a self-awareness tool built for educational purposes. "
    "It is **not** a substitute for professional medical or psychological advice, diagnosis, "
    "or treatment. If you are in crisis, please contact a licensed professional or a helpline "
    "immediately (see the Chatbot page for numbers).",
    icon="⚠️",
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.page_link("pages/1_Mood_Tracker.py", label="📝 Mood Tracker", icon="📝")
    st.write("Journal your day and get instant AI sentiment analysis.")
with col2:
    st.page_link("pages/2_Stress_Quiz.py", label="📊 Stress Quiz", icon="📊")
    st.write("A quick 10-question self-assessment of your current stress level.")
with col3:
    st.page_link("pages/3_Chatbot.py", label="💬 MindMate Chatbot", icon="💬")
    st.write("Talk it out with a friendly supportive chat companion.")
with col4:
    st.page_link("pages/4_Anti_Stress_Games.py", label="🎮 Anti-Stress Games", icon="🎮")
    st.write("Breathing exercise, bubble pop, doodle pad & memory match.")

st.divider()

st.subheader("📈 Your Recent Mood Snapshot")
df = load_mood_log()
if df.empty:
    st.write("No mood entries yet — head to the **Mood Tracker** page to log your first entry!")
else:
    recent = df.tail(7)
    m1, m2, m3 = st.columns(3)
    m1.metric("Entries logged", len(df))
    m2.metric("Latest mood", f"{recent.iloc[-1]['mood_label']}")
    m3.metric("Avg. polarity (last 7)", f"{recent['polarity'].mean():.2f}")
    st.line_chart(df.set_index("timestamp")["polarity"], height=200)

st.divider()
with st.expander("⚙️ Data & Privacy"):
    st.write(
        "All your journal entries and quiz results are stored **locally** in this app's "
        "`data/` folder as CSV files — nothing is sent to any external server."
    )
    if st.button("🗑️ Clear all my saved data", type="secondary"):
        clear_all_data()
        st.success("All local data cleared. Refresh the page to see the change.")

st.caption("Built with Python + Streamlit + TextBlob • Made for academic demonstration purposes.")
