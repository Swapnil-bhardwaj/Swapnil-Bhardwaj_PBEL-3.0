import streamlit as st
import matplotlib.pyplot as plt
from utils.mood_analysis import analyze_entry, mood_score_to_10
from utils.storage import log_mood, load_mood_log

st.set_page_config(page_title="Mood Tracker", page_icon="📝", layout="wide")
st.title("📝 AI Mood Tracker")
st.write(
    "Write freely about your day. Our sentiment-analysis engine (TextBlob NLP) will "
    "estimate your mood and log it so you can spot patterns over time."
)

with st.form("mood_form", clear_on_submit=True):
    entry = st.text_area(
        "How are you feeling right now? What's on your mind?",
        height=150,
        placeholder="e.g. Today was a bit stressful because of my exams, but I felt better after talking to a friend...",
    )
    submitted = st.form_submit_button("Analyze & Save Entry", type="primary")

if submitted:
    if not entry.strip():
        st.warning("Please write something before submitting.")
    else:
        result = analyze_entry(entry)
        log_mood(entry, result.polarity, result.subjectivity, result.mood_label)

        if result.is_crisis_flag:
            st.error(
                "It sounds like you might be going through something really difficult. "
                "You deserve support from a real person right now. Please see the **Chatbot** "
                "page for crisis helpline numbers, or reach out to someone you trust immediately."
            )

        c1, c2, c3 = st.columns(3)
        c1.metric("Detected Mood", f"{result.emoji} {result.mood_label}")
        c2.metric("Wellbeing Score", f"{mood_score_to_10(result.polarity)} / 10")
        c3.metric("Sentiment Polarity", f"{result.polarity:+.2f}")
        st.caption(
            f"Subjectivity: {result.subjectivity:.2f} "
            "(0 = very factual, 1 = very opinion/emotion based)"
        )
        st.success("Entry saved to your mood log below. ✅")

st.divider()
st.subheader("📊 Your Mood History")

df = load_mood_log()
if df.empty:
    st.info("No entries yet. Your history and trend chart will appear here once you log something.")
else:
    tab1, tab2 = st.tabs(["Trend Chart", "Raw Entries"])

    with tab1:
        fig, ax = plt.subplots(figsize=(9, 3.5))
        ax.plot(df["timestamp"], df["polarity"], marker="o", linewidth=1.5, color="#6C5CE7")
        ax.axhline(0, color="gray", linewidth=0.8, linestyle="--")
        ax.set_ylabel("Sentiment polarity (-1 to +1)")
        ax.set_xlabel("Date")
        ax.set_title("Mood trend over time")
        fig.autofmt_xdate(rotation=30)
        st.pyplot(fig)

        mood_counts = df["mood_label"].value_counts()
        st.bar_chart(mood_counts)

    with tab2:
        st.dataframe(
            df.sort_values("timestamp", ascending=False)[
                ["timestamp", "mood_label", "polarity", "subjectivity", "entry"]
            ],
            use_container_width=True,
            hide_index=True,
        )
