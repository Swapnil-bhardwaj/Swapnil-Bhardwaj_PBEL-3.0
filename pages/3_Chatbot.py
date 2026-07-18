import streamlit as st
from utils.chatbot_logic import get_bot_response

st.set_page_config(page_title="MindMate Chatbot", page_icon="💬", layout="wide")
st.title("💬 MindMate — Supportive Chat Companion")
st.caption(
    "A rule-based supportive chatbot. It listens and offers gentle suggestions — "
    "it is not a therapist and cannot replace professional care."
)

with st.expander("☎️ Crisis helplines (India & general)"):
    st.markdown(
        "- **KIRAN Mental Health Helpline (India):** 1800-599-0019 (24/7, toll-free)\n"
        "- **iCall (TISS, India):** 9152987821 (Mon–Sat, 10am–8pm)\n"
        "- Outside India: please search for your country's local crisis line, or go to your "
        "nearest emergency room if you are in immediate danger."
    )

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        ("bot", "Hey there 👋 I'm MindMate. How are you feeling today?")
    ]

for sender, msg in st.session_state.chat_history:
    with st.chat_message("assistant" if sender == "bot" else "user"):
        st.write(msg)

user_msg = st.chat_input("Type how you're feeling...")
if user_msg:
    st.session_state.chat_history.append(("user", user_msg))
    bot_reply = get_bot_response(user_msg)
    st.session_state.chat_history.append(("bot", bot_reply))
    st.rerun()

if st.button("🔄 Clear conversation"):
    st.session_state.chat_history = [
        ("bot", "Hey there 👋 I'm MindMate. How are you feeling today?")
    ]
    st.rerun()
