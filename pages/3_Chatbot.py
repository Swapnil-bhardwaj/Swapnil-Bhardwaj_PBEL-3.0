import streamlit as st
from utils.chatbot_logic import get_bot_response, stream_response_generator
from utils.ui import apply_student_theme, render_student_header, render_footer

st.set_page_config(
    page_title="MindMate Buddy | Polite Student Companion",
    page_icon="💬",
    layout="wide",
)

apply_student_theme()

# --- Sidebar Configuration & Settings ---
with st.sidebar:
    st.markdown("### 🎓 MindMate Settings")
    
    selected_tone = st.selectbox(
        "Conversational Tone:",
        ["Warm & Encouraging", "Practical & Study-Focused", "Calm & Grounding"],
        index=0,
        help="Adjust how MindMate frames advice, encouragement, and study strategies."
    )
    
    with st.expander("🔑 Optional: AI Cloud Key"):
        st.caption(
            "MindMate works **100% locally and offline** by default using our built-in student reasoning engine. "
            "If you wish to enable free open-ended generative AI, you can optionally paste a Google Gemini API key below."
        )
        api_key_input = st.text_input(
            "Gemini API Key:",
            type="password",
            value=st.session_state.get("gemini_api_key", ""),
            placeholder="AIzaSy...",
            help="Get a free key from Google AI Studio (aistudio.google.com). Leave blank for offline mode."
        )
        if api_key_input:
            st.session_state.gemini_api_key = api_key_input.strip()
        else:
            st.session_state.gemini_api_key = ""

    # Mode indicator badge
    if st.session_state.get("gemini_api_key"):
        st.success("⚡ Mode: Generative AI Connected")
    else:
        st.info("💻 Mode: Offline Student Engine (Private & Fast)")

    st.markdown("---")
    
    # Conversation Actions
    if st.button("🔄 Reset Conversation", use_container_width=True, type="secondary"):
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": (
                    "Hello and welcome! It is truly a pleasure to connect with you. 😊 "
                    "I am **MindMate**, your polite campus companion. "
                    "Whether you would like to explore proven study techniques like Pomodoro, discuss exam stress, "
                    "or simply talk through your day, I am right here with you.\n\n"
                    "How may I assist you today?"
                )
            }
        ]
        st.rerun()

    # Export / Copy chat transcript
    if "chat_history" in st.session_state and len(st.session_state.chat_history) > 1:
        transcript = "\n\n".join([
            f"{'MindMate' if m['role'] == 'assistant' else 'You'}: {m['content']}"
            for m in st.session_state.chat_history
        ])
        st.download_button(
            label="📥 Download Chat Transcript",
            data=transcript,
            file_name="mindmate_chat_transcript.txt",
            mime="text/plain",
            use_container_width=True,
        )

# --- Main Page Header ---
render_student_header(
    title="MindMate Peer Companion",
    subtitle="A courteous, respectful, and thoughtful assistant designed to help university students manage stress, master study skills, and navigate campus life.",
    badge="Respectful & Supportive Peer 💬",
)

# Safety Crisis Resources Drawer
with st.expander("☎️ Student Helplines & Emergency Support (Free, Confidential & 24/7)"):
    st.markdown(
        """
        If you or someone you know is in severe distress or needs immediate emotional support:
        - 🇮🇳 **Tele-MANAS (Govt of India):** [14416](tel:14416) or [1800-891-4416](tel:18008914416) *(24/7, Toll-Free)*
        - 🇮🇳 **KIRAN Mental Health Helpline:** [1800-599-0019](tel:18005990019) *(24/7, Toll-Free)*
        - 🇮🇳 **iCall (TISS):** [9152987821](tel:9152987821) *(Mon–Sat, 10:00 AM – 8:00 PM)*
        - 🎓 **Campus Counseling:** Please reach out to your university's student health or counseling center.
        - 🌍 **International:** Please dial your country's local emergency helpline or student medical cell.
        """
    )

# --- Initialize Conversation State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": (
                "Hello and welcome! It is truly a pleasure to connect with you. 😊 "
                "I am **MindMate**, your polite campus companion. "
                "Whether you would like to explore proven study techniques like Pomodoro, discuss exam stress, "
                "or simply talk through your day, I am right here with you.\n\n"
                "How may I assist you today?"
            )
        }
    ]

# --- Quick Topic Starters ---
st.markdown("<div style='font-size: 0.88rem; font-weight: 700; color: #475569; margin-bottom: 6px;'>💡 Quick Topics to Explore:</div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c4, c5, c6 = st.columns(3)
clicked_prompt = None

with c1:
    if st.button("📚 Overcoming Exam Anxiety", key="p_exam", use_container_width=True):
        clicked_prompt = "I am feeling quite stressed and anxious about my upcoming exams."
with c2:
    if st.button("⏱️ How to use Pomodoro", key="p_pomo", use_container_width=True):
        clicked_prompt = "Could you please explain how to effectively use the Pomodoro technique for studying?"
with c3:
    if st.button("🧠 The Feynman Method", key="p_feyn", use_container_width=True):
        clicked_prompt = "Can you please explain how the Feynman Technique works?"
with c4:
    if st.button("⏳ Beating Procrastination", key="p_proc", use_container_width=True):
        clicked_prompt = "I have an assignment due soon, but I am finding it difficult to stop procrastinating."
with c5:
    if st.button("🥱 All-Nighter Recovery", key="p_night", use_container_width=True):
        clicked_prompt = "I pulled an all-nighter studying and I feel completely exhausted."
with c6:
    if st.button("👥 Group Project Challenges", key="p_group", use_container_width=True):
        clicked_prompt = "How can I politely handle teammates in a group project who are not contributing?"

st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

# --- Display Existing Conversation ---
for msg in st.session_state.chat_history:
    avatar = "🎓" if msg["role"] == "assistant" else "🎒"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# --- Process Input (via Text or Starter Button) ---
user_input = st.chat_input("Type your message politely here... (e.g., 'How can I organize my study schedule?')")
prompt_to_process = clicked_prompt or user_input

if prompt_to_process:
    # 1. Render user message
    with st.chat_message("user", avatar="🎒"):
        st.markdown(prompt_to_process)
    
    # 2. Append to history
    st.session_state.chat_history.append({"role": "user", "content": prompt_to_process})
    
    # 3. Generate response with full history context
    api_key = st.session_state.get("gemini_api_key", None)
    bot_reply = get_bot_response(
        text=prompt_to_process,
        history=st.session_state.chat_history[:-1],
        tone=selected_tone,
        api_key=api_key,
    )
    
    # 4. Stream assistant message with typewriter effect
    with st.chat_message("assistant", avatar="🎓"):
        st.write_stream(stream_response_generator(bot_reply))
        
    # 5. Save assistant reply to history
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
    
    # Rerun to clean up state & prompt buttons
    st.rerun()

st.markdown("---")
render_footer()
