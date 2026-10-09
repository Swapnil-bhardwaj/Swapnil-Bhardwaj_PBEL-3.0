import streamlit as st
from utils.quiz_data import QUESTIONS, OPTIONS, MAX_SCORE, score_to_severity
from utils.storage import log_quiz, load_quiz_log
from utils.ui import apply_student_theme, render_student_header, render_footer

st.set_page_config(page_title="Stress Check | MindMate", page_icon="📊", layout="wide")

apply_student_theme()

render_student_header(
    title="Semester Stress & Burnout Check",
    subtitle="Answer honestly based on how the past 2 weeks have felt. A quick pulse check to prevent academic burnout.",
    badge="Self-Assessment 📊",
)

st.info(
    "🔒 **Confidential & Private:** All responses are calculated instantly on your local machine and never transmitted anywhere.",
    icon="🛡️"
)

option_labels = [label for label, _ in OPTIONS]

with st.form("stress_quiz"):
    answers = []
    for i, q in enumerate(QUESTIONS):
        st.markdown(
            f"""
            <div style="background: white; border: 1px solid #E2E8F0; border-radius: 14px; padding: 14px 18px; margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
                <div style="font-weight: 700; color: #1E293B; font-size: 0.98rem; margin-bottom: 6px;">
                    <span style="color: #4F46E5; margin-right: 6px;">Q{i + 1}.</span> {q}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        choice = st.radio(
            f"Select for Q{i + 1}",
            option_labels,
            key=f"q{i}",
            horizontal=True,
            label_visibility="collapsed",
        )
        answers.append(dict(OPTIONS)[choice])

    submitted = st.form_submit_button("Calculate My Stress Level ➔", type="primary")

if submitted:
    score = sum(answers)
    severity, advice, color = score_to_severity(score)
    log_quiz("Academic Stress Check", score, MAX_SCORE, severity)

    st.markdown("<hr style='margin: 1.5rem 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
    
    st.markdown(
        f"""
        <div style="background: white; border: 2px solid {color}; border-radius: 18px; padding: 1.6rem; margin-bottom: 1.5rem; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 14px;">
                <div style="font-size: 1.4rem; font-weight: 800; color: #1E293B;">
                    Result: <span style="color: {color};">{severity}</span>
                </div>
                <div style="background: #F1F5F9; padding: 6px 16px; border-radius: 20px; font-weight: 700; color: #334155; font-size: 0.95rem;">
                    Score: {score} / {MAX_SCORE}
                </div>
            </div>
            <div style="margin-bottom: 14px;">
                <div style="height: 10px; background: #E2E8F0; border-radius: 999px; overflow: hidden;">
                    <div style="width: {int((score/MAX_SCORE)*100)}%; height: 100%; background: {color}; border-radius: 999px; transition: width 0.5s;"></div>
                </div>
            </div>
            <div style="background: #F8FAFC; border-radius: 12px; padding: 14px 18px; font-size: 0.95rem; color: #334155; line-height: 1.55;">
                <strong>Campus Survival Advice:</strong><br>{advice}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr style='margin: 2rem 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
st.subheader("📈 Past Check-In History")
qdf = load_quiz_log()
if qdf.empty:
    st.info("No past quiz results recorded yet. Complete your first check above!")
else:
    col_g1, col_g2 = st.columns([2, 1])
    with col_g1:
        st.line_chart(qdf.set_index("timestamp")["score"], height=220)
    with col_g2:
        st.dataframe(
            qdf.sort_values("timestamp", ascending=False)[["timestamp", "severity", "score"]],
            use_container_width=True,
            hide_index=True,
        )

st.markdown("---")
render_footer()
