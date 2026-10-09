import streamlit as st
import streamlit.components.v1 as components
from utils.ui import apply_student_theme, render_student_header, render_footer
from utils.games import (
    BREATHING_HTML,
    BUBBLE_POP_HTML,
    DOODLE_PAD_HTML,
    MEMORY_GAME_HTML,
    SOUNDSCAPE_HTML,
    ZEN_GARDEN_HTML,
    FORTUNE_COOKIE_HTML,
    RIPPLE_POND_HTML,
)

st.set_page_config(
    page_title="Anti-Stress Games | MindMate",
    page_icon="🎮",
    layout="wide",
)

apply_student_theme()

render_student_header(
    title="Campus Relaxation & Study-Break Hub",
    subtitle="Give your eyes and prefrontal cortex a quick 5-minute breather. Pick an activity below to unwind.",
    badge="Study Break Arcade 🎮",
)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🫁 Box Breathing",
    "🎧 Lo-Fi Soundscapes",
    "🫧 Bubble Pop",
    "🪵 Zen Sand Garden",
    "🥠 Affirmation Cookie",
    "🌊 Ripple Pond",
    "🎨 Doodle Pad",
    "🧩 Memory Match",
])

with tab1:
    st.markdown(
        "**Box Breathing (4-4-4-4):** Used to immediately calm the nervous system before an exam, presentation, or interview. Follow the orb."
    )
    components.html(BREATHING_HTML, height=420, scrolling=False)

with tab2:
    st.markdown(
        "**Procedural Soundscape Mixer:** Mix your ideal background soundscape for studying or falling asleep. Zero buffering, generated live in your browser."
    )
    components.html(SOUNDSCAPE_HTML, height=420, scrolling=False)

with tab3:
    st.markdown(
        "**Bubble Wrap Pop:** Mindless, tactile satisfaction with pop sounds to release physical tension from typing or writing."
    )
    components.html(BUBBLE_POP_HTML, height=450, scrolling=False)

with tab4:
    st.markdown(
        "**Zen Sand Garden:** Rake smooth grooves into sand, place dark river stones, or scatter sakura petals to quiet mental clutter."
    )
    components.html(ZEN_GARDEN_HTML, height=480, scrolling=False)

with tab5:
    st.markdown(
        "**Student Affirmation Cookie:** Feeling imposter syndrome or academic burnout? Crack open a fresh cookie for a grounded reminder."
    )
    components.html(FORTUNE_COOKIE_HTML, height=380, scrolling=False)

with tab6:
    st.markdown(
        "**Calming Ripple Pond:** Tap and drag across the water surface to generate expanding glowing ripples around floating water lilies."
    )
    components.html(RIPPLE_POND_HTML, height=430, scrolling=False)

with tab7:
    st.markdown(
        "**Doodle & Whiteboard:** Scribble your stress away, sketch flowcharts, or download your mini artwork."
    )
    components.html(DOODLE_PAD_HTML, height=480, scrolling=False)

with tab8:
    st.markdown(
        "**Campus Memory Match:** A low-stakes, gentle memory card game to shift your focus away from deadlines."
    )
    components.html(MEMORY_GAME_HTML, height=470, scrolling=False)

st.markdown("---")
render_footer()
