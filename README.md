# 🎓 MindMate — Campus Wellness & Student Mood Companion

A modern, student-centric web app built with Python + Streamlit to help students **navigate academic stress, journal thoughts with sentiment reflection, self-assess semester burnout, chat with an empathetic peer companion, and recharge with 8 anti-stress mini-games** — running 100% locally and privately.

> 🎒 **Built for students, by students:** Clean, relatable, and private. No corporate buzzwords, no cloud tracking, and designed specifically around exam pressure, assignment crunches, and campus life.

---

## ✨ Features & Student Modules

| Module | Description |
|---|---|
| 📝 **Campus Mood Journal** | Vent about difficult lectures, submissions, or small wins with quick context tags (`#ExamCrunch`, `#AllNighter`, `#GroupProject`). Uses NLP sentiment reflection to visualize your emotional trajectory over the semester. |
| 📊 **Semester Stress & Burnout Check** | A 10-question self-assessment tailored for student life (GPA anxiety, sleep issues, screen fatigue, imposter syndrome) with actionable campus survival advice. |
| 💬 **MindMate Peer Buddy** | A supportive chat companion that understands academic dread, procrastination, and roommate drama, with integrated crisis safety helplines. |
| 🎮 **Study Break Hub (8 Games)** | Quick 5-minute study-break activities: Guided Box Breathing, Procedural Lo-Fi Soundscape Mixer, Bubble Wrap Pop, Zen Sand Garden, Student Affirmation Cookie, Calming Water Ripple Pond, Doodle Whiteboard, and Memory Match. |
| 🔒 **100% Local & Private** | All notes and assessment histories stay strictly on your local computer in CSV format. Zero external data tracking. |

---

## 🎮 Study Break Mini-Games

1. **🫁 Guided Box Breathing:** 4s-4s-4s-4s breathing orb designed to calm pre-exam anxiety and reset your nervous system.
2. **🎧 Lo-Fi Soundscapes Mixer:** Web Audio procedural synthesis of rain on library windows, cozy fireplace, ocean waves, and campus crickets with custom volume sliders.
3. **🫧 Bubble Wrap Pop:** Satisfying, colorful bubble popping with synthetic audio pops.
4. **🪵 Zen Sand Garden:** Drag to rake smooth zen grooves in sand, place river stones, or scatter sakura petals.
5. **🥠 Affirmation Cookie:** Interactive cookie that cracks open to reveal supportive reminders about self-worth beyond GPA and handling burnout.
6. **🌊 Calming Ripple Pond:** Tactile interactive water pond with expanding ripples and floating lotuses.
7. **🎨 Doodle Pad:** Whiteboard sketchpad with smooth brushes, custom palette, and PNG export.
8. **🧩 Campus Memory Match:** Low-stakes card matching with student-themed emojis to gently shift focus away from deadlines.

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Streamlit** — Web UI & multipage application framework
- **TextBlob** — Lexicon-based NLP sentiment polarity & subjectivity
- **Pandas & Matplotlib** — Emotional trajectory tracking & visualization
- **HTML5 / CSS3 / Vanilla JavaScript / Web Audio API** — High-performance zero-rerun interactive mini-games

---

## 📁 Project Structure

```
Swapnil-Bhardwaj_PBEL-3.0/
├── app.py                          # Premium student landing page & campus wellness hub
├── pages/
│   ├── 1_Mood_Tracker.py           # Student mood journal + semester charts
│   ├── 2_Stress_Quiz.py            # Academic stress & burnout check
│   ├── 3_Chatbot.py                # Peer chat companion
│   └── 4_Anti_Stress_Games.py      # Study break hub (8 mini-games)
├── utils/
│   ├── ui.py                       # Modern student design system, typography, & affirmations
│   ├── games.py                    # 8 interactive HTML5/JS relaxation games
│   ├── mood_analysis.py            # Sentiment analysis & peer reflections
│   ├── chatbot_logic.py            # Empathetic student conversation rules
│   ├── quiz_data.py                # Student stress questions & scoring
│   └── storage.py                  # Local CSV storage helpers
├── data/                           # Local CSV logs (gitignored)
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone or navigate to the repository
```bash
git clone https://github.com/Swapnil-bhardwaj/Swapnil-Bhardwaj_PBEL-3.0.git
cd Swapnil-Bhardwaj_PBEL-3.0
```

### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 🔒 Confidential Helplines & Student Resources

If you or a friend is in distress or feeling overwhelmed:
- 🇮🇳 **Tele-MANAS:** `14416` or `1800-891-4416` (24/7 National Mental Health Helpline, Toll-Free)
- 🇮🇳 **KIRAN:** `1800-599-0019` (24/7, Toll-Free)
- 🇮🇳 **iCall (TISS):** `9152987821` (Mon–Sat, 10:00 AM – 8:00 PM)
- 🌍 **International:** Please reach out to your local campus counseling cell or emergency services.

---

## 📜 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
