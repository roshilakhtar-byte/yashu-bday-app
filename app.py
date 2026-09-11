"""
🎮 Happy 19th Birthday, Yashu — a gatekeeper + one-question-at-a-time
trivia app.

HOW TO RUN
    pip install streamlit
    streamlit run app.py

CUSTOMIZE
    Song, Shayari, photo links, and the quiz bank are all in the
    block right below the imports. Add more entries to QUESTIONS in
    the same dict shape to grow the quiz — see the note near the
    bottom of that list.
"""

import streamlit as st
import os

# ============================================================
# 🎂 CUSTOMIZE THESE 🎂
# ============================================================
NICKNAME = "Yashu"

# Pick one — "3 am thoughts" by Naalayak, or "Slipping Through My Fingers"
TRACK_PATH = "Cigarettes After Sex - K. (Live on KEXP) - KEXP (youtube).mp3"  # <-- put the chosen song here, same folder as this script

SHAYARI = """
[Paste your Shayari for Yashu here —
each line will show up exactly as you write it.]
"""

# Paste real photo URLs (or local filenames) here, one per caption below
GALLERY = [
    {"url": "PASTE_PHOTO_URL_1", "caption": "The Sad Constant Face"},
    {"url": "PASTE_PHOTO_URL_2", "caption": "God of Organic Chem"},
    {"url": "PASTE_PHOTO_URL_3", "caption": "Team Conrad Enthusiast"},
    {"url": "PASTE_PHOTO_URL_4", "caption": "VMC Patna Veteran"},
    {"url": "PASTE_PHOTO_URL_5", "caption": "Restaurant Pour Tous Regular"},
    {"url": "PASTE_PHOTO_URL_6", "caption": "NIT Delhi Era"},
]

# Quiz bank — add more dicts in this exact shape to grow past 10.
# correct_index is 0-based, pointing into "options".
QUESTIONS = [
    {
        "question": "What school did Yashu attend before the JEE grind began?",
        "options": ["Don Bosco Patna", "St. Xavier's", "Delhi Public School", "Notre Dame Academy"],
        "correct_index": 0,
    },
    {
        "question": "Which coaching institute shaped Yashu's JEE years?",
        "options": ["Allen Kota", "VMC Patna", "FIITJEE", "Aakash Institute"],
        "correct_index": 1,
    },
    {
        "question": "Which subject did Yashu ascend to godhood in during his Drop Year?",
        "options": ["Physics", "Mathematics", "Organic Chemistry", "Biology"],
        "correct_index": 2,
    },
    {
        "question": "Where is Yashu currently pursuing his degree?",
        "options": ["IIT Delhi", "DTU", "NIT Delhi", "NSUT"],
        "correct_index": 2,
    },
    {
        "question": "What's Yashu studying at NIT Delhi?",
        "options": ["Computer Science", "Mechanical Engineering", "Civil Engineering", "Electrical Engineering"],
        "correct_index": 3,
    },
    {
        "question": "Which artist is basically the soundtrack of Yashu's every mood?",
        "options": ["Cigarettes After Sex", "Imagine Dragons", "Arctic Monkeys", "Coldplay"],
        "correct_index": 0,
    },
    {
        "question": "What's the holy pilgrimage site Yashu introduced to the group?",
        "options": ["A random McDonald's", "Restaurant Pour Tous", "A 24-hour dhaba", "Domino's"],
        "correct_index": 1,
    },
    {
        "question": "What's Yashu's default facial expression, no matter the occasion?",
        "options": ["The Sad Constant Face", "A huge grin", "A confused squint", "A wink"],
        "correct_index": 0,
    },
    {
        "question": "Which side is Yashu loyal to?",
        "options": ["Team Conrad", "Team Jeremiah", "Strictly neutral", "Doesn't watch the show"],
        "correct_index": 0,
    },
    {
        "question": "What was Yashu's era right before Organic Chem godhood?",
        "options": ["A chess prodigy", "A theatre kid", "A humble VMC Patna JEE aspirant", "A sports captain"],
        "correct_index": 2,
    },
    # Add more questions here in the same shape to grow the quiz.
]
# ============================================================

st.set_page_config(
    page_title=f"Happy 19th, {NICKNAME}!",
    page_icon="🖤",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------- SESSION STATE ----------------
for key, default in [
    ("user_identity", None),
    ("quiz_index", 0),
    ("score", 0),
    ("answered", False),
    ("last_correct", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ---------------- CUSTOM CSS ----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .stApp {
        background: radial-gradient(circle at 20% 10%, #241a1a 0%, #120d0f 45%, #0a0708 100%);
        color: #e9ddc9;
    }

    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 900px;
        margin: 0 auto;
    }

    h1, h2, h3, h4 {
        font-family: 'Cormorant Garamond', serif;
        color: #e7c99b;
        letter-spacing: 0.02em;
    }

    p, li, span, label {
        color: #d9cdb8;
    }

    .hero-card {
        background: linear-gradient(160deg, rgba(60,40,35,0.55), rgba(20,14,15,0.55));
        border: 1px solid rgba(231,201,155,0.25);
        border-radius: 18px;
        padding: 36px 28px;
        text-align: center;
        margin-bottom: 22px;
    }

    .hero-card h1 { font-size: 2.6rem; margin-bottom: 6px; }

    .terminal-line {
        font-family: 'JetBrains Mono', monospace;
        color: #a68a63;
        font-size: 0.9rem;
        letter-spacing: 0.03em;
        margin-bottom: 4px;
    }

    .shayari-card {
        background: rgba(255,255,255,0.03);
        border-left: 3px solid #a3673f;
        border-radius: 4px 14px 14px 4px;
        padding: 24px 28px;
        margin: 18px 0;
        white-space: pre-line;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.3rem;
        line-height: 1.9;
        color: #f0e4cc;
    }

    .gallery-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(231,201,155,0.15);
        border-radius: 14px;
        padding: 10px;
        text-align: center;
        margin-bottom: 16px;
    }

    .gallery-caption {
        font-family: 'Cormorant Garamond', serif;
        color: #e7c99b;
        font-size: 1.05rem;
        margin-top: 8px;
    }

    div[data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255,255,255,0.04);
        padding: 6px;
        border-radius: 14px;
        margin-bottom: 14px;
    }

    button[data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: #b8a98c;
        padding: 8px 16px;
        font-weight: 600;
        border: none;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #a3673f, #5c3a2e);
        color: #fceee0 !important;
    }

    button[data-baseweb="tab"] p { color: inherit; }

    .stTextInput input {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(231,201,155,0.3);
        border-radius: 10px;
        color: #f0e4cc;
        padding: 10px 14px;
    }

    .stButton button {
        background: linear-gradient(135deg, #a3673f, #5c3a2e);
        color: #fceee0 !important;
        border: none;
        border-radius: 999px;
        padding: 10px 30px;
        font-weight: 600;
        transition: transform 0.15s ease;
    }
    .stButton button:hover { transform: scale(1.03); }

    div[role="radiogroup"] label {
        background: rgba(255,255,255,0.04);
        border-radius: 8px;
        padding: 6px 14px;
        margin-bottom: 4px;
    }

    div[data-testid="stAlert"] { border-radius: 12px; }

    div[data-testid="stProgress"] > div > div {
        background-color: #a3673f;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["🏠 The Welcome Mat", "📸 The Yashu Vault", "🎮 The Ultimate Trial"])

# ============================================================
# TAB 1 — THE WELCOME MAT
# ============================================================
with tab1:
    st.markdown(
        f"""
        <div class="hero-card">
            <h1>Happy 19th Birthday, {NICKNAME}! 🖤</h1>
            <p>Nineteen trips around the sun, still perfecting that moody stare.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<p class="terminal-line">&gt; before we proceed, who is accessing this terminal?</p>', unsafe_allow_html=True)
    identity_choice = st.radio(
        " ",
        ["I am Yashasvi (The Birthday Boy)", "I am one of the Boys"],
        index=None,
        key="identity_radio",
        label_visibility="collapsed",
    )
    if identity_choice:
        st.session_state.user_identity = "yashasvi" if identity_choice.startswith("I am Yashasvi") else "boys"
        st.success(f"Access granted. Welcome, {'Yashasvi' if st.session_state.user_identity == 'yashasvi' else 'friend'}.")

    st.markdown("#### 🎧 Setting the mood")
    if os.path.exists(TRACK_PATH):
        st.audio(TRACK_PATH)
    else:
        st.info(
            f"🎵 Drop '3 am thoughts' (Naalayak) or 'Slipping Through My Fingers' here as "
            f"`{TRACK_PATH}` and it'll play right on this tab."
        )

    st.markdown("#### For you")
    st.markdown(f'<div class="shayari-card">{SHAYARI}</div>', unsafe_allow_html=True)

# ============================================================
# TAB 2 — THE YASHU VAULT
# ============================================================
with tab2:
    st.markdown("## 📸 The Yashu Vault")
    st.write("Evidence, curated.")

    cols = st.columns(3)
    for i, item in enumerate(GALLERY):
        with cols[i % 3]:
            st.markdown('<div class="gallery-card">', unsafe_allow_html=True)
            if item["url"] and not item["url"].startswith("PASTE_"):
                st.image(item["url"], use_container_width=True)
            else:
                st.image(f"https://picsum.photos/seed/yashu{i}/400/400", use_container_width=True)
            st.markdown(f'<p class="gallery-caption">{item["caption"]}</p>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    st.caption("Swap the placeholder URLs in GALLERY at the top of the script with real photo links.")

# ============================================================
# TAB 3 — THE ULTIMATE TRIAL
# ============================================================
with tab3:
    st.markdown("## 🎮 The Ultimate Trial")

    if st.session_state.user_identity is None:
        st.warning("Head back to **The Welcome Mat** and tell us who's playing first.")
    else:
        total = len(QUESTIONS)
        idx = st.session_state.quiz_index

        if idx < total:
            q = QUESTIONS[idx]
            st.progress(idx / total)
            st.markdown(f"**Question {idx + 1} of {total}**")
            st.markdown(f"### {q['question']}")

            selected = st.radio(
                "Your answer:",
                q["options"],
                index=None,
                key=f"quiz_radio_{idx}",
                label_visibility="collapsed",
            )

            if not st.session_state.answered:
                if st.button("Submit Answer", key=f"submit_{idx}"):
                    if selected is None:
                        st.warning("Pick an answer first.")
                    else:
                        st.session_state.answered = True
                        is_correct = selected == q["options"][q["correct_index"]]
                        st.session_state.last_correct = is_correct
                        if is_correct:
                            st.session_state.score += 1
                        st.rerun()

            if st.session_state.answered:
                if st.session_state.last_correct:
                    st.success("Correct! 🎉")
                elif st.session_state.user_identity == "yashasvi":
                    st.error("Bro, how do you forget your own lore? Did Organic Chem finally break your brain?")
                else:
                    st.error("Fake friend alert! Hand over your BMC OG group membership right now.")

                button_label = "Next Question ➡️" if idx + 1 < total else "See Final Score 🏁"
                if st.button(button_label, key=f"next_{idx}"):
                    st.session_state.quiz_index += 1
                    st.session_state.answered = False
                    st.session_state.last_correct = None
                    st.rerun()
        else:
            st.balloons()
            pct = st.session_state.score / total
            st.markdown(f"## 🏆 Final Score: {st.session_state.score} / {total}")
            if pct == 1:
                st.success("Perfect score. Certified Yashu scholar. Happy birthday, legend.")
            elif pct >= 0.6:
                st.info("Solid effort. You clearly pay attention.")
            else:
                st.warning("Rough. Time to spend more time with the birthday boy.")

            if st.button("Play Again"):
                st.session_state.quiz_index = 0
                st.session_state.score = 0
                st.session_state.answered = False
                st.session_state.last_correct = None
                st.rerun()
