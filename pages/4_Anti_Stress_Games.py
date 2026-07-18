import streamlit as st
import streamlit.components.v1 as components
from utils.games import BREATHING_HTML, BUBBLE_POP_HTML, DOODLE_PAD_HTML, MEMORY_GAME_HTML

st.set_page_config(page_title="Anti-Stress Games", page_icon="🎮", layout="wide")
st.title("🎮 Anti-Stress Games")
st.write("A few minutes of play can genuinely lower stress. Pick one below and take a short break.")

tab1, tab2, tab3, tab4 = st.tabs(
    ["🫁 Breathing Exercise", "🫧 Bubble Pop", "🎨 Doodle Pad", "🧩 Memory Match"]
)

with tab1:
    st.write("Follow the circle: expands on **inhale**, holds, shrinks on **exhale**, holds. This is the classic *box breathing* technique used to calm the nervous system.")
    components.html(BREATHING_HTML, height=340, scrolling=False)

with tab2:
    st.write("Pop every bubble on the sheet — a satisfying, mindless little win.")
    components.html(BUBBLE_POP_HTML, height=430, scrolling=False)

with tab3:
    st.write("Doodle freely, pick a color and brush size, and download your creation when you're done.")
    components.html(DOODLE_PAD_HTML, height=470, scrolling=False)

with tab4:
    st.write("A calm little card-matching game to gently occupy your mind.")
    components.html(MEMORY_GAME_HTML, height=520, scrolling=False)
