import streamlit as st
import matplotlib.pyplot as plt
from utils.mood_analysis import analyze_entry, mood_score_to_10
from utils.storage import log_mood, load_mood_log
from utils.ui import apply_student_theme, render_student_header, render_footer

st.set_page_config(page_title="Mood Journal | MindMate", page_icon="📝", layout="wide")

apply_student_theme()

render_student_header(
    title="Campus Mood Journal",
    subtitle="Unpack your day without judgment. Whether you're drowning in submissions or celebrating an A, write it out.",
    badge="Personal Journal 📝",
)

st.markdown(
    """
    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px; padding: 1rem 1.2rem; margin-bottom: 1.4rem;">
        <span style="font-weight: 700; color: #334155;">💡 Student Journal Prompts:</span>
        <span style="color: #64748B; font-size: 0.92rem;">
            How did your lectures feel today? • Any looming deadlines stressing you out? • What's one small win or highlight?
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("mood_form", clear_on_submit=True):
    col_tags1, col_tags2 = st.columns([2, 1])
    with col_tags1:
        entry = st.text_area(
            "What's on your mind right now?",
            height=140,
            placeholder="e.g. Spent 4 hours debugging code for my submission tomorrow. Felt like pulling my hair out, but finally got the test cases passing! Grabbing some midnight chai with my roommate now...",
        )
    with col_tags2:
        st.markdown("<div style='font-size: 0.88rem; font-weight: 600; color: #475569; margin-bottom: 6px;'>🏷️ Quick Context Tags:</div>", unsafe_allow_html=True)
        tags = st.multiselect(
            "Select relevant tags:",
            [
                "📚 Exam Crunch",
                "💻 Coding / Lab",
                "👥 Group Project",
                "☕ Caffeine Fuel",
                "🌙 All-Nighter",
                "🏠 Hostel / Mess",
                "🫂 Friends Hangout",
                "🥱 Burnout / Exhausted",
                "🎉 Small Win",
            ],
            placeholder="Choose tags...",
            label_visibility="collapsed"
        )

    submitted = st.form_submit_button("Log Entry & Reflect ✨", type="primary")

if submitted:
    if not entry.strip():
        st.warning("Please type a thought or reflection before submitting.")
    else:
        full_text = entry.strip()
        if tags:
            tag_str = " [" + ", ".join(tags) + "]"
            full_text = f"{full_text}{tag_str}"

        result = analyze_entry(full_text)
        log_mood(full_text, result.polarity, result.subjectivity, result.mood_label)

        if result.is_crisis_flag:
            st.error(
                "💙 **We hear you, and you don't have to carry this alone.** "
                "It sounds like you're going through something really painful right now. "
                "Please reach out to a trusted friend, family member, or call one of the free campus/national helplines "
                "listed on the **MindMate Buddy** page right now."
            )

        st.markdown(
            f"""
            <div style="background: white; border: 1px solid #E2E8F0; border-radius: 18px; padding: 1.4rem; margin-top: 1rem; box-shadow: 0 4px 16px rgba(0,0,0,0.04);">
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; margin-bottom: 12px;">
                    <div>
                        <span style="font-size: 1.8rem; margin-right: 8px;">{result.emoji}</span>
                        <span style="font-size: 1.3rem; font-weight: 700; color: #1E293B;">{result.mood_label}</span>
                    </div>
                    <div style="background: #EEF2FF; color: #4F46E5; font-weight: 700; padding: 6px 14px; border-radius: 20px; font-size: 0.95rem;">
                        Wellbeing Index: {mood_score_to_10(result.polarity)} / 10
                    </div>
                </div>
                <div style="background: #F8FAFC; border-left: 4px solid #6366F1; padding: 12px 16px; border-radius: 8px; color: #334155; font-size: 0.95rem; line-height: 1.5;">
                    <strong>Peer Note:</strong> {result.student_reflection}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.toast("Journal entry saved locally! 📝", icon="✅")

st.markdown("<hr style='margin: 2rem 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

st.subheader("📊 Your Semester Mood Curve")

df = load_mood_log()
if df.empty:
    st.info("No journal entries logged yet. Write your first thought above to begin charting your semester journey.")
else:
    tab1, tab2 = st.tabs(["📈 Mood Trajectory", "📜 Journal Archive"])

    with tab1:
        c_left, c_right = st.columns([2, 1])
        with c_left:
            fig, ax = plt.subplots(figsize=(9, 4), facecolor="none")
            ax.set_facecolor("#FAFAFC")
            ax.plot(
                range(len(df)),
                df["polarity"],
                marker="o",
                color="#4F46E5",
                linewidth=2.5,
                markersize=6,
                label="Mood Sentiment",
            )
            ax.axhline(0, color="#94A3B8", linewidth=1, linestyle="--", label="Baseline (Neutral)")
            ax.set_ylabel("Sentiment Polarity (-1 to +1)", fontsize=10, color="#475569")
            ax.set_title("Emotional Trend Over Logged Days", fontsize=12, fontweight="bold", color="#1E293B")
            ax.grid(True, linestyle=":", alpha=0.6, color="#CBD5E1")
            ax.set_xticks(range(len(df)))
            ax.set_xticklabels([ts.split()[0] if " " in str(ts) else str(ts) for ts in df["timestamp"]], rotation=25, ha="right", fontsize=8)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#CBD5E1')
            ax.spines['bottom'].set_color('#CBD5E1')
            plt.tight_layout()
            st.pyplot(fig)

        with c_right:
            st.markdown("<div style='font-weight: 700; color: #1E293B; margin-bottom: 8px;'>Mood Breakdown:</div>", unsafe_allow_html=True)
            mood_counts = df["mood_label"].value_counts()
            st.bar_chart(mood_counts, color="#6366F1")

    with tab2:
        st.markdown(f"**Total Entries Logged:** {len(df)}")
        st.dataframe(
            df.sort_values("timestamp", ascending=False)[
                ["timestamp", "mood_label", "polarity", "entry"]
            ],
            use_container_width=True,
            hide_index=True,
        )

st.markdown("---")
render_footer()
