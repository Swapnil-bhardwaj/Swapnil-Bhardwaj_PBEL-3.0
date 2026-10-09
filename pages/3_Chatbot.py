import streamlit as st
from utils.chatbot_logic import get_bot_response
from utils.ui import apply_student_theme, render_student_header, render_footer

st.set_page_config(page_title="MindMate Buddy | Chat", page_icon="💬", layout="wide")

apply_student_theme()

render_student_header(
    title="MindMate Peer Buddy",
    subtitle="A warm, confidential chat companion who gets student life. Vent about coursework, late nights, or tricky deadlines.",
    badge="Supportive Peer Chat 💬",
)

with st.expander("☎️ Student Helplines & Emergency Support (Free & Confidential)"):
    st.markdown(
        """
        - 🇮🇳 **Tele-MANAS (Govt of India):** `14416` or `1800-891-4416` (24/7, Toll-Free)
        - 🇮🇳 **KIRAN Mental Health Helpline:** `1800-599-0019` (24/7, Toll-Free)
        - 🇮🇳 **iCall (TISS):** `9152987821` (Mon–Sat, 10:00 AM – 8:00 PM)
        - 🎓 **Campus Support:** Check your university's student wellness or counseling cell.
        - 🌍 **International:** Call your country's local emergency helpline or student emergency services.
        """
    )

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        ("bot", "Hey there! 👋 I'm MindMate. Whether you're drowning in lab reports, stressing over midterms, or just need to vent, I'm here. What's on your mind today?")
    ]

# Suggested prompt starter chips
st.markdown("<div style='font-size: 0.85rem; font-weight: 600; color: #64748B; margin-bottom: 6px;'>💡 Quick Starters:</div>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
clicked_prompt = None

with c1:
    if st.button("📚 Stressed about exams", key="p_exam", use_container_width=True):
        clicked_prompt = "I'm feeling really stressed about my upcoming exams."
with c2:
    if st.button("⏳ Can't stop procrastinating", key="p_proc", use_container_width=True):
        clicked_prompt = "I have an assignment due soon but I can't stop procrastinating."
with c3:
    if st.button("🥱 Exhausted from all-nighter", key="p_night", use_container_width=True):
        clicked_prompt = "I pulled an all-nighter and I feel completely exhausted."
with c4:
    if st.button("👥 Group project drama", key="p_group", use_container_width=True):
        clicked_prompt = "My group project teammates are not doing their part."

# Handle clicked prompt if any
if clicked_prompt:
    st.session_state.chat_history.append(("user", clicked_prompt))
    reply = get_bot_response(clicked_prompt)
    st.session_state.chat_history.append(("bot", reply))
    st.rerun()

st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

# Render conversation
for sender, msg in st.session_state.chat_history:
    if sender == "bot":
        with st.chat_message("assistant", avatar="🎓"):
            st.markdown(msg)
    else:
        with st.chat_message("user", avatar="🎒"):
            st.markdown(msg)

user_msg = st.chat_input("Talk to your buddy... (e.g. feeling nervous about tomorrow's viva)")
if user_msg:
    st.session_state.chat_history.append(("user", user_msg))
    bot_reply = get_bot_response(user_msg)
    st.session_state.chat_history.append(("bot", bot_reply))
    st.rerun()

st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
if st.button("🔄 Start Fresh Conversation", type="secondary"):
    st.session_state.chat_history = [
        ("bot", "Hey there! 👋 I'm MindMate. What's on your mind today?")
    ]
    st.rerun()

render_footer()
