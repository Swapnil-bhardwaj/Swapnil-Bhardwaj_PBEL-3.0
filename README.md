# 🧠 MindMate — AI-Based Mental Health Monitoring Solution

A Python + Streamlit web app that helps users **track their mood using AI sentiment analysis**,
**self-assess their stress level**, **chat with a supportive rule-based chatbot**, and **unwind
with anti-stress mini-games** — all in one place, running fully locally.

> ⚠️ **Disclaimer:** This is an educational/academic project. It is **not** a medical device and
> does not diagnose any condition. It is a self-awareness tool only. If you or someone you know is
> in crisis, please contact a licensed professional or a helpline immediately.

---

## ✨ Features

| Module | Description |
|---|---|
| 📝 **Mood Tracker** | Journal your thoughts; TextBlob-based NLP scores sentiment (polarity/subjectivity) and logs mood trend over time with charts |
| 📊 **Stress Self-Assessment** | 10-question Likert-style quiz that scores your current stress level and gives tailored advice |
| 💬 **MindMate Chatbot** | Rule-based supportive chatbot that responds empathetically, and surfaces crisis helpline info if concerning keywords are detected |
| 🎮 **Anti-Stress Games** | 4 relaxing mini-games: guided box-breathing exercise, bubble pop, doodle pad, and memory match |
| 💾 **Local Data Storage** | All mood/quiz history saved locally as CSV — nothing leaves your machine |

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Streamlit** — web UI & multipage app framework
- **TextBlob** — lexicon-based sentiment analysis (the "AI" in mood detection)
- **Pandas** — data logging & analysis
- **Matplotlib** — mood trend charts
- **Vanilla HTML/CSS/JS** — embedded via Streamlit components for the anti-stress games

---

## 📁 Project Structure

```
mental-health-monitor/
├── app.py                          # Home page
├── pages/
│   ├── 1_Mood_Tracker.py           # AI mood journal + sentiment charts
│   ├── 2_Stress_Quiz.py            # Stress self-assessment quiz
│   ├── 3_Chatbot.py                # Supportive chatbot UI
│   └── 4_Anti_Stress_Games.py      # Games tab (breathing/bubble/doodle/memory)
├── utils/
│   ├── mood_analysis.py            # Sentiment analysis logic (TextBlob)
│   ├── chatbot_logic.py            # Rule-based chatbot responses
│   ├── quiz_data.py                # Quiz questions + scoring
│   ├── storage.py                  # CSV read/write helpers
│   └── games.py                    # HTML/JS for the 4 mini-games
├── data/                           # Local CSV logs (auto-created, gitignored)
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone or download this project
```bash
git clone https://github.com/<your-username>/mental-health-monitor.git
cd mental-health-monitor
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 📤 Pushing This Project to GitHub

If you haven't already created a repository on GitHub, do that first (on github.com, click
**New repository**, name it e.g. `mental-health-monitor`, and **don't** initialize it with a
README since you already have one here).

Then, from inside this project folder, run:

```bash
git init
git add .
git commit -m "Initial commit: AI-based mental health monitoring solution"
git branch -M main
git remote add origin https://github.com/<your-username>/mental-health-monitor.git
git push -u origin main
```

> Replace `<your-username>` with your actual GitHub username and repo name.
> If prompted for credentials and you have 2FA enabled, use a
> [Personal Access Token](https://github.com/settings/tokens) instead of your password.

**Updating later**, after making changes:
```bash
git add .
git commit -m "Describe what you changed"
git push
```

---

## 🧩 How the "AI" Works

- **Sentiment Analysis:** `TextBlob` uses a lexicon-based approach (pattern analyzer) to score text
  polarity (-1 to +1) and subjectivity (0 to 1). The app buckets polarity into 5 mood categories
  (Very Low → Very Good) and converts it into a friendlier 0–10 wellbeing score.
- **Stress Scoring:** A weighted-sum scoring model (0–3 per question × 10 questions = 0–30 total)
  maps to 4 severity bands, each with tailored guidance.
- **Chatbot:** Keyword/pattern matching maps user messages to empathetic response categories
  (stress, anxiety, sadness, loneliness, etc.), with a dedicated crisis-keyword safety net that
  overrides normal chat and surfaces helpline numbers.

This keeps the project fully explainable (useful for a viva/demo) without needing to train or ship
a large ML model — you can swap in a trained scikit-learn/transformers classifier later in
`utils/mood_analysis.py` if you want to extend it.

---

## 🔮 Possible Extensions

- Swap TextBlob for a fine-tuned transformer model (e.g. DistilBERT sentiment) for more nuance
- Add user authentication for multi-user support (currently single-user/local)
- Move CSV storage to SQLite/PostgreSQL
- Add voice journal input using speech-to-text
- Deploy to Streamlit Community Cloud for a live demo link

---

## 📜 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Crisis Resources

If you or someone you know is struggling:
- **India — KIRAN Mental Health Helpline:** 1800-599-0019 (24/7, toll-free)
- **India — iCall (TISS):** 9152987821 (Mon–Sat, 10am–8pm)
- Outside India, please search for your local crisis helpline, or go to your nearest emergency room.
