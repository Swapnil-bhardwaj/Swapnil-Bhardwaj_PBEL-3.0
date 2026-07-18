import streamlit as st
from utils.quiz_data import QUESTIONS, OPTIONS, MAX_SCORE, score_to_severity
from utils.storage import log_quiz, load_quiz_log

st.set_page_config(page_title="Stress Quiz", page_icon="📊", layout="wide")
st.title("📊 Stress Self-Assessment")
st.write(
    "Answer based on **the last 2 weeks**. This is a short self-awareness check, "
    "not a clinical diagnosis."
)

option_labels = [label for label, _ in OPTIONS]

with st.form("stress_quiz"):
    answers = []
    for i, q in enumerate(QUESTIONS):
        choice = st.radio(f"**{i + 1}. {q}**", option_labels, key=f"q{i}", horizontal=True)
        answers.append(dict(OPTIONS)[choice])
    submitted = st.form_submit_button("See My Results", type="primary")

if submitted:
    score = sum(answers)
    severity, advice = score_to_severity(score)
    log_quiz("Stress Self-Assessment", score, MAX_SCORE, severity)

    st.divider()
    st.subheader("Your Results")
    c1, c2 = st.columns(2)
    c1.metric("Total Score", f"{score} / {MAX_SCORE}")
    c2.metric("Stress Level", severity)
    st.progress(score / MAX_SCORE)

    if severity == "High stress":
        st.error(advice)
    elif severity == "Moderate stress":
        st.warning(advice)
    else:
        st.success(advice)

    st.caption(
        "Remember: this tool is for self-awareness only. If you're concerned about your "
        "mental health, please speak with a qualified professional."
    )

st.divider()
st.subheader("📈 Past Quiz Results")
qdf = load_quiz_log()
if qdf.empty:
    st.info("No past quiz results yet.")
else:
    st.line_chart(qdf.set_index("timestamp")["score"], height=200)
    st.dataframe(
        qdf.sort_values("timestamp", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
