import streamlit as st
import random
import time
from cases import cases

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="The Detective's Dossier",
    page_icon="🕵️",
    layout="wide"
)

# ---------------------------
# LOAD CSS
# ---------------------------
def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception:
        pass

load_css()

# ---------------------------
# SESSION STATE INIT
# ---------------------------
defaults = {
    "started": False,
    "score": 0,
    "round": 1,
    "start_time": time.time(),
    "step": 0,
    "case": None,
    "selected_suspect": "",
    "reasoning": "",
    "selected_room": None,
    "visited_rooms": [],
    "revealed_clues": {},
    "unlocked_rooms": [],
    "lock_attempts": {},
    "puzzle_attempts": {},
    "hints_used": 0,
    "accusation_suspect": None,
    "logic_grid_done": False,
    "logic_grid_result": None,
    "logic_grid_state": {},
    "difficulty": "Easy",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------------------
# HELPERS
# ---------------------------
def step_bar(current: int, total: int = 3):
    dots = ""
    for i in range(total):
        cls = "done" if i < current else ("active" if i == current else "")
        dots += f'<div class="step-dot {cls}"></div>'
    labels = ["📂 Case File", "🗺️ Investigate", "⚖️ Verdict"]
    st.markdown(
        f'<div class="step-bar">{dots}</div>'
        f'<p style="font-size:0.75rem;color:var(--text-muted);margin:0 0 16px 0;">'
        f'Step {current+1}/{total} — {labels[min(current,2)]}</p>',
        unsafe_allow_html=True
    )

def new_case(difficulty_label, exclude=None):
    diff = difficulty_label.lower()
    pool = [c for c in cases if c["difficulty"] == diff]
    if exclude and len(pool) > 1:
        pool = [c for c in pool if c["title"] != exclude.get("title")]
    if not pool:
        pool = [c for c in cases if c["difficulty"] == diff]
    return random.choice(pool)

def reset_investigation():
    st.session_state.selected_room = None
    st.session_state.visited_rooms = []
    st.session_state.revealed_clues = {}
    st.session_state.unlocked_rooms = []
    st.session_state.lock_attempts = {}
    st.session_state.puzzle_attempts = {}
    st.session_state.hints_used = 0
    st.session_state.accusation_suspect = None
    st.session_state.selected_suspect = ""
    st.session_state.reasoning = ""
    st.session_state.logic_grid_done = False
    st.session_state.logic_grid_result = None
    st.session_state.logic_grid_state = {}

def check_answer(user_input: str, correct: str) -> bool:
    return user_input.strip().lower() == correct.strip().lower()

def clue_box(text: str, correct: bool):
    color = "#22c55e" if correct else "#ef4444"
    icon  = "📋" if correct else "⚠️"
    st.markdown(f"""
        <div style='background:var(--bg-card);border:1px solid var(--border-color);
            border-left:4px solid {color};border-radius:2px;
            padding:10px 14px;color:{color};
            font-family:"Courier Prime",monospace;font-size:0.9rem;margin-top:8px;'>
        {icon} {text}
        </div>
    """, unsafe_allow_html=True)

def info_box(text: str, accent: str = "#3a6ea5"):
    st.markdown(f"""
        <div style='background:var(--bg-card);border:1px solid {accent};
            border-radius:2px;padding:10px 14px;
            color:var(--text-primary);font-family:"Courier Prime",monospace;
            font-size:0.9rem;margin:6px 0;line-height:1.6;'>
        {text}
        </div>
    """, unsafe_allow_html=True)

# ---------------------------
# CAESAR CIPHER HELPER (sidebar)
# ---------------------------
def caesar_cipher_sidebar():
    with st.expander("🔢 Caesar Cipher Helper"):
        st.markdown("""
**To decode:** shift each letter BACK by the number given.

**Shift +2** (subtract 2): C→A, D→B, E→C, F→D, G→E, H→F, I→G, J→H, K→I, L→J, M→K, N→L, O→M, P→N, Q→O, R→P, S→Q, T→R, U→S, V→T, W→U, X→V, Y→W, Z→X

**Shift +3** (subtract 3): D→A, E→B, F→C, G→D, H→E, I→F, J→G, K→H, L→I, M→J, N→K, O→L, P→M, Q→N, R→O, S→P, T→Q, U→R, V→S, W→T, X→U, Y→V, Z→W

**Shift +4** (subtract 4): E→A, F→B, G→C, H→D, I→E, J→F, K→G, L→H, M→I, N→J, O→K, P→L, Q→M, R→N, S→O, T→P, U→Q, V→R, W→S, X→T, Y→U, Z→V

**Reversed text:** read the string backwards, letter by letter.
        """)

# ---------------------------
# PUZZLE RENDERERS
# ---------------------------
def render_lock(room_data: dict) -> bool:
    name = room_data["name"]
    lock = room_data.get("lock")
    if not lock:
        return True
    if name in st.session_state.unlocked_rooms:
        return True

    attempts = st.session_state.lock_attempts.get(name, 0)
    st.markdown(f"""
        <div style='background:var(--bg-danger);border:2px solid #ef4444;
            border-radius:4px;padding:16px 20px;margin:12px 0;'>
        <p style='color:#ef4444;font-family:"Special Elite",cursive;
            font-size:1.1rem;margin:0 0 12px 0;'>🔐 LOCKED ROOM</p>
        <p style='color:var(--text-primary);font-family:"Courier Prime",monospace;
            white-space:pre-line;'>{lock['question']}</p>
        </div>
    """, unsafe_allow_html=True)

    if attempts >= 1:
        st.caption(f"💡 Hint: {lock['hint']}")

    user_ans = st.text_input("Enter the answer to unlock:", key=f"lock_input_{name}", placeholder="Type your answer...")
    col1, _ = st.columns([1, 3])
    with col1:
        if st.button("🔓 Unlock", key=f"lock_btn_{name}"):
            st.session_state.lock_attempts[name] = attempts + 1
            if check_answer(user_ans, lock["answer"]):
                st.session_state.unlocked_rooms.append(name)
                st.success("✅ Correct! Room unlocked.")
                st.rerun()
            else:
                st.error("❌ Wrong answer. Try again.")
                st.rerun()
    return False


def render_puzzle(room_data: dict, difficulty_label: str):
    name   = room_data["name"]
    puzzle = room_data.get("puzzle")
    diff   = difficulty_label.lower()

    # Easy mode: no puzzles
    if diff == "easy":
        if name not in st.session_state.revealed_clues:
            if st.button("🔦 Examine Evidence", key=f"examine_{name}"):
                st.session_state.revealed_clues[name] = "true"
                st.rerun()
        else:
            clue_box(room_data["clue_revealed"], correct=True)
        return

    # No puzzle defined
    if not puzzle:
        if name not in st.session_state.revealed_clues:
            if st.button("🔦 Examine Evidence", key=f"examine_{name}"):
                st.session_state.revealed_clues[name] = "true"
                st.rerun()
        else:
            clue_box(room_data["clue_revealed"], correct=True)
        return

    # Already answered
    if name in st.session_state.revealed_clues:
        was_correct = st.session_state.revealed_clues[name] == "true"
        text = room_data["clue_revealed"] if was_correct else room_data.get("false_clue", "Misleading clue recorded.")
        clue_box(text, correct=was_correct)
        return

    attempts = st.session_state.puzzle_attempts.get(name, 0)
    ptype    = puzzle["type"]

    st.markdown(f"""
        <div style='background:var(--bg-card);border:2px solid #e2c97e;
            border-radius:4px;padding:16px 20px;margin:12px 0;'>
        <p style='color:#e2c97e;font-family:"Special Elite",cursive;
            font-size:1rem;margin:0 0 10px 0;'>
        {"🧩 RIDDLE" if ptype == "riddle" else "🔢 CIPHER"} — Solve to reveal evidence
        </p>
        <p style='color:var(--text-primary);font-family:"Courier Prime",monospace;
            white-space:pre-line;line-height:1.7;'>{puzzle['question']}</p>
        </div>
    """, unsafe_allow_html=True)

    if ptype == "cipher" and "cipher_text" in puzzle:
        st.markdown(f"""
            <div style='background:var(--bg-card);border:1px solid #3a6ea5;
                border-radius:2px;padding:10px 16px;margin:8px 0;
                font-family:"Courier Prime",monospace;font-size:1.1rem;
                color:#e2c97e;letter-spacing:3px;text-align:center;'>
            {puzzle['cipher_text']}
            </div>
        """, unsafe_allow_html=True)

    if attempts >= 1:
        st.caption(f"💡 Hint: {puzzle['hint']}")

    user_ans = st.text_input("Your answer:", key=f"puzzle_input_{name}", placeholder="Type your answer...")
    col1, col2, _ = st.columns([1, 1, 3])
    with col1:
        if st.button("✅ Submit", key=f"puzzle_submit_{name}"):
            st.session_state.puzzle_attempts[name] = attempts + 1
            if check_answer(user_ans, puzzle["answer"]):
                st.session_state.revealed_clues[name] = "true"
                st.success("✅ Correct! Evidence unlocked.")
                st.rerun()
            else:
                st.session_state.revealed_clues[name] = "false"
                st.error("❌ Wrong — a misleading clue has been logged.")
                st.rerun()
    with col2:
        if st.button("⏭️ Skip", key=f"puzzle_skip_{name}"):
            st.session_state.score = max(0, st.session_state.score - 5)
            st.session_state.revealed_clues[name] = "true"
            st.info("Skipped (−5 pts). True clue revealed.")
            st.rerun()


def render_logic_grid(case: dict):
    grid_data = case.get("logic_grid")
    if not grid_data:
        return True

    if st.session_state.logic_grid_done:
        result = st.session_state.logic_grid_result
        clue   = grid_data["reward_clue"] if result == "correct" else grid_data["false_clue"]
        clue_box(f"Grid conclusion: {clue}", correct=(result == "correct"))
        return True

    attribute_info = {
        "Left dinner table for 15+ min":  {"emoji": "🚪", "tooltip": "Left the dinner table"},
        "Has financial problems":          {"emoji": "💰", "tooltip": "Financial troubles"},
        "Was alone in Drawing Room":       {"emoji": "🛋️", "tooltip": "Was alone in Drawing Room"},
        "Heavy coat pocket":               {"emoji": "🧥", "tooltip": "Heavy coat pocket"},
        "Kitchen alibi":                   {"emoji": "🍳", "tooltip": "Has kitchen alibi"},
        "On site after 1 AM":             {"emoji": "🌙", "tooltip": "On site after 1 AM"},
        "Has supervisor system access":    {"emoji": "💻", "tooltip": "Supervisor system access"},
        "Fingerprint on canister":         {"emoji": "👆", "tooltip": "Fingerprint on canister"},
        "Left before midnight":            {"emoji": "⏰", "tooltip": "Left before midnight"},
        "Co-signed insurance":             {"emoji": "📝", "tooltip": "Co-signed insurance"},
        "Delivered the whisky":            {"emoji": "🥃", "tooltip": "Delivered the whisky"},
        "Named in new will":               {"emoji": "📜", "tooltip": "Named in new will"},
        "Has chemistry knowledge":         {"emoji": "🧪", "tooltip": "Has chemistry knowledge"},
        "Phone alibi in library":          {"emoji": "📱", "tooltip": "Phone alibi in library"},
        "No motive found":                 {"emoji": "❓", "tooltip": "No motive found"},
    }

    attributes    = grid_data["attributes"]
    suspects      = grid_data["suspects"]
    compact_attrs = [
        attribute_info.get(a, {"emoji": "📌", "tooltip": a})
        for a in attributes
    ]

    if not st.session_state.logic_grid_state:
        st.session_state.logic_grid_state = {s: [False] * len(attributes) for s in suspects}

    # Header panel
    st.markdown(f"""
        <div style='background:var(--bg-card);border:2px solid #3a6ea5;
            border-top:3px solid #e2c97e;border-radius:4px;
            padding:12px 16px 8px 16px;margin:8px 0 4px 0;'>
        <p style='color:#e2c97e;font-family:"Special Elite",cursive;
            font-size:1rem;margin:0 0 4px 0;'>📊 LOGIC GRID</p>
        <p style='color:var(--text-muted);font-family:"Courier Prime",monospace;
            font-size:0.75rem;margin:0;'>{grid_data['intro']}</p>
        </div>
    """, unsafe_allow_html=True)

    # Header row — same columns as data rows so they stay aligned
    header_cols = st.columns([2] + [1] * len(attributes))
    header_cols[0].markdown(
        "<p style='font-family:\"Courier Prime\",monospace;"
        "font-size:0.75rem;color:var(--text-muted);margin:4px 0;"
        "text-transform:uppercase;letter-spacing:1px;'>Suspect</p>",
        unsafe_allow_html=True
    )
    for i, a in enumerate(compact_attrs):
        tooltip = a["tooltip"]
        emoji   = a["emoji"]
        header_cols[i + 1].markdown(
            f"<p style='text-align:center;font-size:1.1rem;margin:4px 0;"
            f"cursor:help;' title='{tooltip}'>{emoji}</p>",
            unsafe_allow_html=True
        )

    # Data rows
    for s in suspects:
        row_cols = st.columns([2] + [1] * len(attributes))
        row_cols[0].markdown(
            f"<p style='font-family:\"Courier Prime\",monospace;"
            f"font-size:0.82rem;color:var(--text-primary);margin:6px 0;'><b>{s}</b></p>",
            unsafe_allow_html=True
        )
        for i in range(len(attributes)):
            current = st.session_state.logic_grid_state[s][i]
            with row_cols[i + 1]:
                # Show ✅ when checked, ☐ (a visible empty box) when unchecked
                label = "✅" if current else "◻️"
                if st.button(label, key=f"grid_{s}_{i}", use_container_width=True):
                    st.session_state.logic_grid_state[s][i] = not current
                    st.rerun()

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    col_btn, col_tip = st.columns([1, 2])
    with col_btn:
        if st.button("📤 Submit Grid", key="submit_grid", use_container_width=True):
            correct_map = grid_data["correct"]
            all_correct = all(
                st.session_state.logic_grid_state[s] == correct_map[s]
                for s in suspects
            )
            st.session_state.logic_grid_done   = True
            st.session_state.logic_grid_result = "correct" if all_correct else "wrong"
            st.rerun()
    with col_tip:
        st.markdown("**Hover over symbols to see what they mean!**")

    return False


# ---------------------------
# SIDEBAR
# ---------------------------
with st.sidebar:
    st.markdown("## 🕵️ The dossier")
    # difficulty_label comes from session state (set on landing page)
    difficulty_label = st.session_state.difficulty

    st.markdown("---")

    # Player Stats — collapsible
    with st.expander("📊 Player Stats", expanded=True):
        elapsed = int(time.time() - st.session_state.start_time)
        minutes, seconds = divmod(elapsed, 60)

        def sidebar_stat(emoji, label, value):
            return f"""<div style='display:flex;align-items:center;justify-content:space-between;
                padding:8px 4px;border-bottom:1px solid var(--border-color);'>
                <span style='font-size:1.1rem;margin-right:8px;'>{emoji}</span>
                <span style='font-family:"Courier Prime",monospace;font-size:0.8rem;
                    color:var(--text-muted);flex:1;'>{label}</span>
                <span style='font-family:"Special Elite",cursive;font-size:1.1rem;
                    color:var(--text-heading);font-weight:bold;'>{value}</span>
            </div>"""

        st.markdown(
            sidebar_stat("🏆", "Score", st.session_state.score) +
            sidebar_stat("🔁", "Cases Solved", st.session_state.round - 1) +
            sidebar_stat("⏱️", "Time", f"{minutes:02d}:{seconds:02d}"),
            unsafe_allow_html=True
        )

    # Hints — collapsible, only during investigation
    if st.session_state.step == 1 and st.session_state.case:
        with st.expander("💡 Hints", expanded=True):
            case_s    = st.session_state.case
            hints     = case_s.get("hints", [])
            used      = st.session_state.hints_used
            remaining = len(hints) - used
            st.caption(f"{remaining} hint(s) remaining")
            if used < len(hints):
                if st.button("🔍 Use Hint (−3 pts)"):
                    st.session_state.hints_used += 1
                    st.session_state.score = max(0, st.session_state.score - 3)
                    st.rerun()
            for i in range(used):
                st.info(f"💡 {hints[i]}")

    # Puzzle Legend — collapsible
    if st.session_state.step == 1 and st.session_state.case:
        with st.expander("🧩 Puzzle Legend"):
            if difficulty_label == "Easy":
                st.markdown(
                    "<p style='font-size:0.8rem;line-height:1.8;'>"
                    "🔍 Easy mode: No puzzles — just investigate!<br>"
                    "✅ Green = true evidence<br>"
                    "⚠️ Red = misleading clue</p>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    "<p style='font-size:0.8rem;line-height:1.8;'>"
                    "🔐 Red border = locked room<br>"
                    "🧩 Amber = riddle puzzle<br>"
                    "🔢 Amber = cipher puzzle<br>"
                    "✅ Green = correct answer<br>"
                    "⚠️ Red = misleading clue<br>"
                    "⏭️ Skip = −5 pts, true clue shown</p>",
                    unsafe_allow_html=True
                )

        # Caesar Cipher Helper — always accessible during investigation
        caesar_cipher_sidebar()

    if st.session_state.started:
        st.markdown("---")
        if st.button("🔄 Restart Game"):
            for k in list(defaults.keys()):
                st.session_state[k] = defaults[k]
            st.rerun()


# ---------------------------
# LANDING PAGE
# ---------------------------
if not st.session_state.started:
    st.markdown("""
        <div style="text-align:center; padding: 40px 0 20px 0;">
            <h1 class='title-glow' style='font-size:2.8rem; letter-spacing:3px;'>
                🕵️ THE DETECTIVES DOSSIER
            </h1>
            <p style='color:var(--text-muted); font-size:1.1rem; letter-spacing:2px;'>
                DETECTIVE SYSTEM v4.0 — INITIALIZING...
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Investigation board photo helper
    def pinned_photo(img_path: str, rotate: float, caption: str, extra_style: str = ""):
        import base64, pathlib
        try:
            data = base64.b64encode(pathlib.Path(img_path).read_bytes()).decode()
            ext  = pathlib.Path(img_path).suffix.lstrip(".")
            mime = "jpeg" if ext in ("jpg", "jpeg") else ext
            src  = f"data:image/{mime};base64,{data}"
        except Exception:
            return ""
        return f"""
        <div style='
            transform: rotate({rotate}deg);
            display: inline-block;
            background: #f8f4ec;
            padding: 10px 10px 32px 10px;
            box-shadow: 4px 5px 16px rgba(0,0,0,0.5), inset 0 0 0 1px rgba(0,0,0,0.06);
            margin: 24px auto 8px auto;
            position: relative;
            border: 1px solid #e0d8cc;
            {extra_style}
        '>
            <img src="{src}" style='width:100%;display:block;filter:sepia(12%) contrast(1.04) brightness(0.97);'>
            <div style='
                font-family:"Courier Prime",monospace;
                font-size:0.6rem;
                color:#5a4a3a;
                text-align:center;
                margin-top:10px;
                letter-spacing:1px;
                text-transform:uppercase;
                opacity:0.85;
            '>{caption}</div>
            <div style='
                position:absolute;
                top:-14px;
                left:calc(50% - 9px);
                width:18px;
                height:18px;
                border-radius:50%;
                background: radial-gradient(circle at 38% 32%, #ffaaaa 5%, #e02020 42%, #7a0000 100%);
                box-shadow: 0 4px 8px rgba(0,0,0,0.6), inset 0 -2px 4px rgba(0,0,0,0.35), inset 3px 2px 4px rgba(255,200,200,0.4);
            '></div>
        </div>"""

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.markdown("<div style='padding-top:30px'>", unsafe_allow_html=True)
        st.markdown(pinned_photo(
            "30ea5fc43e2df8a2050fc523b1a5ad8d.jpg",
            rotate=-4.5, caption="Evidence #001 — Fingerprint Record"
        ), unsafe_allow_html=True)
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown(pinned_photo(
            "ee731fcbb5f03f7bd2ffb4e9b82c8010.jpg",
            rotate=3.2, caption="Crime Scene — Body Outline"
        ), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # Difficulty selector on landing page
        landing_diff = st.selectbox(
            "Select Difficulty",
            ["Easy", "Medium", "Hard"],
            index=["Easy", "Medium", "Hard"].index(st.session_state.difficulty),
            key="landing_difficulty"
        )
        st.session_state.difficulty = landing_diff

        st.markdown("""
            <div class='case-header fade-in'>
            <h3 style='margin-top:0'>📋 Mission Brief</h3>
            <ul style='color:var(--text-primary); line-height:2.2; font-family:"Courier Prime",monospace;'>
                <li>📂 Read the case file</li>
                <li>🗺️ Explore crime scene rooms to collect evidence</li>
                <li>📊 Fill in the logic grid as you discover facts</li>
                <li>🔐 Solve puzzles in Medium / Hard mode</li>
                <li>⚠️ Wrong answers give <strong>misleading clues</strong></li>
                <li>⏭️ Skip a puzzle for −5 pts</li>
                <li>⚖️ Accuse the correct culprit when ready</li>
            </ul>
            <p style='color:#e2c97e; margin-top:16px;'><strong>Easy:</strong> No puzzles — pure investigation.</p>
            <p style='color:#e2c97e;'><strong>Medium / Hard:</strong> Riddles and ciphers guard the evidence.</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🟢 ENTER THE SYSTEM", use_container_width=True):
            st.session_state.started    = True
            st.session_state.start_time = time.time()
            st.rerun()

    with col3:
        st.markdown("<div style='padding-top:30px'>", unsafe_allow_html=True)
        st.markdown(pinned_photo(
            "c8256962b41adbc4775a80c4231d2881.jpg",
            rotate=4.0, caption="Suspect — Unknown"
        ), unsafe_allow_html=True)
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown(pinned_photo(
            "389c0cb7654a21b979ded8ec40b06cba.jpg",
            rotate=-3.0, caption="Scene — Fire"
        ), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()


# ---------------------------
# CASE SELECTION
# ---------------------------
difficulty_label = st.session_state.difficulty
current_case     = st.session_state.case
if (
    current_case is None
    or not current_case.get("rooms")
    or current_case.get("difficulty") != difficulty_label.lower()
):
    st.session_state.case = new_case(difficulty_label)
    reset_investigation()

case = st.session_state.case
if not case or not case.get("rooms"):
    st.error("Failed to load case. Please refresh the page.")
    st.stop()


# ---------------------------
# STEP 0: Case File
# ---------------------------
if st.session_state.step == 0:
    step_bar(0, 3)
    env = case["environment"]
    st.markdown(f"""
        <div class='case-header fade-in'>
            <p style='color:var(--text-muted);font-size:0.8rem;letter-spacing:2px;margin:0 0 4px 0;'>
                CASE #{st.session_state.round:03d} — {case['difficulty'].upper()} — {env['location'].upper()}
            </p>
            <h2 style='margin:0 0 16px 0;'>📂 {case['title']}</h2>
            <p style='color:var(--text-primary);font-size:1.05rem;line-height:1.8;'>{case['story']}</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**📍 Location:** {env['location']}")
        st.markdown(f"**🕐 Time:** {env['time']}")
    with col2:
        st.markdown(f"**🌧️ Weather:** {env['weather']}")
        st.markdown(f"**🔊 Sounds:** {env['sounds']}")
    with col3:
        st.markdown(f"**🧑 Suspects:** {', '.join(case['suspects'].keys())}")
        st.markdown(f"**🏆 Reward:** {case['reward_points']} base pts")

    st.markdown("<br>", unsafe_allow_html=True)
    _, col_btn, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button("🔍 Begin Investigation →", use_container_width=True):
            st.session_state.start_time = time.time()
            st.session_state.step = 1
            st.rerun()


# ---------------------------
# STEP 1: Investigation + Logic Grid
# ---------------------------
elif st.session_state.step == 1:
    step_bar(1, 3)

    rooms      = case["rooms"]
    env        = case["environment"]
    visited    = st.session_state.visited_rooms
    active     = st.session_state.selected_room

    # Three-column layout: map | divider | grid
    col_map, col_div, col_grid = st.columns([2.5, 0.05, 1.5])

    # ── LEFT: Floor plan + room detail ──────────────────────────
    with col_map:

        max_x = max(r["grid_x"] for r in rooms) + 1
        max_y = max(r["grid_y"] for r in rooms) + 1

        st.markdown(f"""
            <div style='background:var(--bg-card);border:2px solid var(--border-color);
                border-top:3px solid #3a6ea5;border-radius:4px;
                padding:12px 16px 0 16px;'>
            <p style='color:#4a8ec8;font-size:0.7rem;letter-spacing:2px;margin:0 0 12px 0;'>
            ▪ FLOOR PLAN — {env["location"].upper()} ▪
            </p>
        """, unsafe_allow_html=True)

        for y in range(max_y):
            cols = st.columns(max_x)
            for x in range(max_x):
                room = next((r for r in rooms if r["grid_x"] == x and r["grid_y"] == y), None)
                with cols[x]:
                    if room:
                        name      = room["name"]
                        is_locked = room.get("locked", False) and name not in st.session_state.unlocked_rooms
                        is_active = (active == name)
                        is_visited= name in visited
                        clue_state= st.session_state.revealed_clues.get(name)

                        cell_class = "room-cell"
                        if is_active:   cell_class += " active"
                        elif is_visited: cell_class += " visited"

                        badge = ("🔐 " if is_locked else
                                 "✅ " if clue_state == "true" else
                                 "⚠️ " if clue_state == "false" else
                                 "👁 " if is_visited else "")

                        st.markdown(f"""
                            <div class='{cell_class}'>
                                <span class='room-icon'>{room['icon']}</span>
                                <span class='room-name'>{badge}{name}</span>
                            </div>
                        """, unsafe_allow_html=True)

                        if st.button("Enter", key=f"room_{x}_{y}"):
                            st.session_state.selected_room = name
                            if name not in st.session_state.visited_rooms:
                                st.session_state.visited_rooms.append(name)
                            st.rerun()
                    else:
                        st.markdown("""
                            <div style='background:repeating-linear-gradient(
                                45deg,#0d1520,#0d1520 6px,#111a26 6px,#111a26 12px);
                                border:1px solid #1a2535;border-radius:2px;min-height:90px;'>
                            </div>
                        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Room detail panel
        st.markdown("### 🔍 Current Location")

        if active:
            room_data = next((r for r in rooms if r["name"] == active), None)
            if room_data:
                if room_data.get("locked", False):
                    if not render_lock(room_data):
                        st.stop()

                col_img, col_info = st.columns([2, 3])
                with col_img:
                    img = room_data.get("image_url", "")
                    if img and img != "YOUR_PHOTO_HERE":
                        st.image(img, caption=f"📷 {room_data['name']}", use_container_width=True)
                    else:
                        st.markdown(f"""
                            <div style='background:var(--bg-card);border:2px dashed var(--border-color);
                                border-radius:4px;height:200px;display:flex;
                                align-items:center;justify-content:center;'>
                            <span style='font-size:3rem;'>{room_data['icon']}</span>
                            </div>
                        """, unsafe_allow_html=True)

                with col_info:
                    st.markdown(f"### {room_data['icon']} {room_data['name']}")
                    info_box(room_data["description"])
                    st.markdown(f"""
                        <div style='background:var(--bg-amber);border:1px solid #e2c97e;
                            border-radius:2px;padding:8px 14px;margin:8px 0;
                            color:#e2c97e;font-size:0.88rem;
                            font-family:"Courier Prime",monospace;'>
                        🔍 Object: <strong>{room_data['object']}</strong>
                        </div>
                    """, unsafe_allow_html=True)
                    render_puzzle(room_data, difficulty_label)

                if "suspect" in room_data:
                    sname = room_data["suspect"]
                    sinfo = case["suspects"].get(sname)
                    if sinfo:
                        st.markdown(f"""
                            <div style='background:var(--bg-card);border-left:3px solid #e2c97e;
                                padding:12px;margin:12px 0;border-radius:2px;'>
                                <strong>👤 {sname}</strong> — {sinfo['description']}
                                <blockquote style='color:var(--text-muted);margin-top:8px;'>"{random.choice(sinfo['dialogue'])}"</blockquote>
                            </div>
                        """, unsafe_allow_html=True)

        else:
            st.info("👆 Click **Enter** beneath any room on the blueprint to investigate.")

        # ── ACCUSE BUTTON — always visible during investigation ──────────
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        if st.button("⚖️ Ready to Accuse? →", use_container_width=True, type="primary"):
            st.session_state.step = 2
            st.rerun()

        # Progress metrics — custom HTML cards to avoid emoji/label/number overlap
        st.markdown("<br>", unsafe_allow_html=True)
        visited_count = len(st.session_state.visited_rooms)
        true_clues    = sum(1 for v in st.session_state.revealed_clues.values() if v == "true")
        false_clues   = sum(1 for v in st.session_state.revealed_clues.values() if v == "false")
        hints_used    = st.session_state.hints_used

        def stat_card(emoji, label, value):
            return f"""
                <div style='background:var(--bg-card);border:1px solid var(--border-color);
                    border-radius:4px;padding:10px 12px;text-align:center;'>
                    <div style='font-size:1.3rem;margin-bottom:4px;'>{emoji}</div>
                    <div style='font-size:0.7rem;color:var(--text-muted);
                        font-family:"Courier Prime",monospace;
                        text-transform:uppercase;letter-spacing:0.5px;
                        margin-bottom:6px;'>{label}</div>
                    <div style='font-size:1.4rem;font-family:"Special Elite",cursive;
                        color:var(--text-heading);'>{value}</div>
                </div>"""

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(stat_card("🚪", "Visited",    f"{visited_count}/{len(rooms)}"), unsafe_allow_html=True)
        c2.markdown(stat_card("✅", "True Clues", true_clues),                      unsafe_allow_html=True)
        c3.markdown(stat_card("⚠️", "False",      false_clues),                     unsafe_allow_html=True)
        c4.markdown(stat_card("💡", "Hints",      hints_used),                      unsafe_allow_html=True)

    # ── DIVIDER ──────────────────────────────────────────────────
    with col_div:
        st.markdown("""
            <div style='border-left:1px solid #2a4a6a;height:100%;min-height:600px;margin:0 auto;width:1px;'></div>
        """, unsafe_allow_html=True)

    # ── RIGHT: Logic Grid ─────────────────────────────────────────
    with col_grid:
        render_logic_grid(case)


# ---------------------------
# STEP 2: Accusation
# ---------------------------
elif st.session_state.step == 2:
    step_bar(2, 3)
    st.markdown("## ⚖️ Make Your Accusation")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 🧑 Suspects")
        suspect_options = list(case["suspects"].keys())
        selected = st.radio("Select the guilty suspect:", suspect_options, key="final_accusation")
        reasoning_input = st.text_area(
            "Your reasoning (optional)",
            placeholder="Explain why you believe this suspect is guilty...",
            key="reasoning_input_final",
            height=100
        )
        if st.button("🎯 MAKE ACCUSATION", use_container_width=True, type="primary"):
            st.session_state.selected_suspect = selected
            st.session_state.reasoning = reasoning_input or "Accused based on evidence collected."
            st.session_state.step = 3
            st.rerun()

    with col2:
        st.markdown("### 📋 Evidence Summary")
        visited_count = len(st.session_state.visited_rooms)
        true_clues    = sum(1 for v in st.session_state.revealed_clues.values() if v == "true")
        false_clues   = sum(1 for v in st.session_state.revealed_clues.values() if v == "false")
        info_box(
            f"<b>Rooms investigated:</b> {visited_count}/{len(case['rooms'])}<br>"
            f"<b>True clues found:</b> {true_clues}<br>"
            f"<b>Misleading clues:</b> {false_clues}<br>"
            f"<b>Hints used:</b> {st.session_state.hints_used}<br>"
            f"<b>Logic grid:</b> {st.session_state.logic_grid_result or 'Not submitted'}"
        )
        false_rooms = [r for r, v in st.session_state.revealed_clues.items() if v == "false"]
        if false_rooms:
            st.warning(f"⚠️ Misleading clues received in: {', '.join(false_rooms)}")


# ---------------------------
# STEP 3: Verdict Result
# ---------------------------
elif st.session_state.step == 3:
    step_bar(3, 3)
    correct    = case["answer"]
    selected   = st.session_state.selected_suspect
    time_taken = int(time.time() - st.session_state.start_time)
    minutes, seconds = divmod(time_taken, 60)
    is_correct = (selected == correct)
    false_count = sum(1 for v in st.session_state.revealed_clues.values() if v == "false")

    if is_correct:
        speed_bonus   = max(60 - time_taken, 0)
        hint_penalty  = st.session_state.hints_used * 3
        false_penalty = false_count * 5
        points = max(case.get("reward_points", 10) + speed_bonus - hint_penalty - false_penalty, 1)
        st.session_state.score += points
        st.markdown(f"""
            <div class='verdict-correct fade-in'>
                <h2 class='glow'>✔ CASE CLOSED</h2>
                <p style='color:var(--text-primary);font-size:1.1rem;'>
                    Correct. <strong>{correct}</strong> is the culprit.
                </p>
                <p style='color:#22c55e;font-size:1.4rem;font-weight:bold;'>+{points} points</p>
                <p style='color:var(--text-muted);font-size:0.85rem;'>
                    Base: {case['reward_points']} | Speed: +{speed_bonus} |
                    Hints: −{hint_penalty} | Misleads: −{false_penalty}
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class='verdict-wrong fade-in'>
                <h2 style='color:#ef4444;'>✗ WRONG ACCUSATION</h2>
                <p style='color:var(--text-primary);font-size:1.1rem;'>
                    You accused <strong>{selected}</strong>.
                    The real culprit was <strong>{correct}</strong>.
                </p>
                <p style='color:#ef4444;'>No points awarded.</p>
                {f"<p style='color:var(--text-muted);font-size:0.85rem;'>You followed {false_count} misleading clue(s).</p>" if false_count else ""}
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🧠 Case Explanation")
        info_box(case.get("explanation", "No explanation available."), accent="#e2c97e")
    with col2:
        st.markdown("### 📋 Your Investigation")
        grid_result = st.session_state.logic_grid_result or "not submitted"
        info_box(
            f"⏱️ Time: {minutes:02d}:{seconds:02d}<br>"
            f"🚪 Rooms visited: {len(st.session_state.visited_rooms)}/{len(case['rooms'])}<br>"
            f"✅ True clues: {sum(1 for v in st.session_state.revealed_clues.values() if v == 'true')}<br>"
            f"⚠️ Misleading clues: {false_count}<br>"
            f"📊 Logic grid: {grid_result}<br>"
            f"💡 Hints used: {st.session_state.hints_used}<br><br>"
            f"<em>\"{st.session_state.reasoning}\"</em>"
        )

    if st.session_state.revealed_clues:
        st.markdown("### 🔎 Evidence You Collected")
        for rname, result in st.session_state.revealed_clues.items():
            rd = next((r for r in case["rooms"] if r["name"] == rname), None)
            if rd:
                was_correct = result == "true"
                text = rd["clue_revealed"] if was_correct else rd.get("false_clue", "Misleading clue.")
                icon_str = rd['icon']
                clue_box(f"{icon_str} <strong>{rname}:</strong> {text}", correct=was_correct)

    st.markdown("<br>", unsafe_allow_html=True)
    # Difficulty progression: Easy → Medium → Hard → Hard (stays at Hard)
    diff_order   = ["Easy", "Medium", "Hard"]
    current_idx  = diff_order.index(difficulty_label) if difficulty_label in diff_order else 0
    next_diff    = diff_order[min(current_idx + 1, len(diff_order) - 1)]
    btn_label    = f"📁 Next Case → ({next_diff})" if next_diff != difficulty_label else "📁 Next Case →"

    if st.button(btn_label, use_container_width=True):
        st.session_state.round      += 1
        st.session_state.step        = 0
        st.session_state.difficulty  = next_diff
        st.session_state.case        = new_case(next_diff, exclude=case)
        reset_investigation()
        st.rerun()