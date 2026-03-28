import streamlit as st
import random
import time
from cases import cases

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Crime Solver Pro",
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
        f'<p style="font-size:0.75rem;color:#94afc8;margin:0 0 16px 0;">'
        f'Step {current+1}/{total} — {labels[min(current,2)]}</p>',
        unsafe_allow_html=True
    )

def new_case(difficulty, exclude=None):
    pool = [c for c in cases if c["difficulty"] == difficulty]
    if exclude and len(pool) > 1:
        pool = [c for c in pool if c != exclude]
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
    if correct:
        color, border, icon = "#22c55e", "#22c55e", "📋"
    else:
        color, border, icon = "#ef4444", "#ef4444", "⚠️"
    st.markdown(f"""
        <div style='background:#0a1628;border:1px solid #1e3a5f;
            border-left:4px solid {border};border-radius:2px;
            padding:10px 14px;color:{color};
            font-family:"Courier Prime",monospace;font-size:0.9rem;margin-top:8px;'>
        {icon} {text}
        </div>
    """, unsafe_allow_html=True)

def info_box(text: str, accent: str = "#3a6ea5"):
    st.markdown(f"""
        <div style='background:#0f1e30;border:1px solid {accent};
            border-radius:2px;padding:10px 14px;
            color:#c8d6e5;font-family:"Courier Prime",monospace;
            font-size:0.9rem;margin:6px 0;line-height:1.6;'>
        {text}
        </div>
    """, unsafe_allow_html=True)

# ---------------------------
# CAESAR CIPHER HELPER
# ---------------------------
def caesar_cipher_helper():
    """Display a Caesar cipher helper in an expander"""
    with st.expander("🔢 Caesar Cipher Helper - Click to Open"):
        st.markdown("""
**How to decode a Caesar cipher:**

Each letter is shifted forward by a certain number. To decode, shift BACK by that number.

**Example (shift +3):**
- A → D, B → E, C → F, etc.
- To decode: D → A, E → B, F → C

**Alphabet reference:**
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25

**Quick shift table (shift +3):**

| Encoded | Decoded | Encoded | Decoded |
|---------|---------|---------|---------|
| D | A | Q | N |
| E | B | R | O |
| F | C | S | P |
| G | D | T | Q |
| H | E | U | R |
| I | F | V | S |
| J | G | W | T |
| K | H | X | U |
| L | I | Y | V |
| M | J | Z | W |
| N | K | | |
| O | L | | |
| P | M | | |

**Shift +2 table:**

| Encoded | Decoded | Encoded | Decoded |
|---------|---------|---------|---------|
| C | A | O | M |
| D | B | P | N |
| E | C | Q | O |
| F | D | R | P |
| G | E | S | Q |
| H | F | T | R |
| I | G | U | S |
| J | H | V | T |
| K | I | W | U |
| L | J | X | V |
| M | K | Y | W |
| N | L | Z | X |
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
        <div style='background:#1a0a0a;border:2px solid #ef4444;
            border-radius:4px;padding:16px 20px;margin:12px 0;'>
        <p style='color:#ef4444;font-family:"Special Elite",cursive;
            font-size:1.1rem;margin:0 0 12px 0;'>🔐 LOCKED ROOM</p>
        <p style='color:#c8d6e5;font-family:"Courier Prime",monospace;
            white-space:pre-line;'>{lock['question']}</p>
        </div>
    """, unsafe_allow_html=True)

    if attempts >= 1:
        st.caption(f"💡 Hint: {lock['hint']}")

    user_ans = st.text_input("Enter the answer to unlock:", key=f"lock_input_{name}", placeholder="Type your answer...")
    col1, col2 = st.columns([1, 3])
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

def render_puzzle(room_data: dict, difficulty: str):
    name = room_data["name"]
    puzzle = room_data.get("puzzle")

    if difficulty == "easy":
        if name not in st.session_state.revealed_clues:
            if st.button("🔦 Examine Evidence", key=f"examine_{name}"):
                st.session_state.revealed_clues[name] = "true"
                st.rerun()
        else:
            clue_box(room_data["clue_revealed"], correct=True)
        return

    if not puzzle:
        if name not in st.session_state.revealed_clues:
            if st.button("🔦 Examine Evidence", key=f"examine_{name}"):
                st.session_state.revealed_clues[name] = "true"
                st.rerun()
        else:
            clue_box(room_data["clue_revealed"], correct=True)
        return

    if name in st.session_state.revealed_clues:
        was_correct = st.session_state.revealed_clues[name] == "true"
        text = room_data["clue_revealed"] if was_correct else room_data.get("false_clue", "Misleading clue recorded.")
        clue_box(text, correct=was_correct)
        return

    attempts = st.session_state.puzzle_attempts.get(name, 0)
    ptype = puzzle["type"]

    st.markdown(f"""
        <div style='background:#0a1628;border:2px solid #e2c97e;
            border-radius:4px;padding:16px 20px;margin:12px 0;'>
        <p style='color:#e2c97e;font-family:"Special Elite",cursive;
            font-size:1rem;margin:0 0 10px 0;'>
        {"🧩 RIDDLE" if ptype == "riddle" else "🔢 CIPHER"} — Solve to reveal evidence
        </p>
        <p style='color:#c8d6e5;font-family:"Courier Prime",monospace;
            white-space:pre-line;line-height:1.7;'>{puzzle['question']}</p>
        </div>
    """, unsafe_allow_html=True)

    if ptype == "cipher":
        caesar_cipher_helper()
        if "cipher_text" in puzzle:
            st.markdown(f"""
                <div style='background:#111827;border:1px solid #3a6ea5;
                    border-radius:2px;padding:10px 16px;margin:8px 0;
                    font-family:"Courier Prime",monospace;font-size:1.1rem;
                    color:#e2c97e;letter-spacing:3px;text-align:center;'>
                {puzzle['cipher_text']}
                </div>
            """, unsafe_allow_html=True)

    if attempts >= 1:
        st.caption(f"💡 Hint: {puzzle['hint']}")

    user_ans = st.text_input("Your answer:", key=f"puzzle_input_{name}", placeholder="Type your answer...")
    col1, col2, col3 = st.columns([1, 1, 3])
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
        clue = grid_data["reward_clue"] if result == "correct" else grid_data["false_clue"]
        clue_box(f"Grid conclusion: {clue}", correct=(result == "correct"))
        return True

    # Define attribute emojis and tooltips
    attribute_info = {
        "Left dinner table for 15+ min": {"emoji": "🚪", "tooltip": "Left the dinner table"},
        "Has financial problems": {"emoji": "💰", "tooltip": "Financial troubles"},
        "Was alone in Drawing Room": {"emoji": "🛋️", "tooltip": "Was alone in Drawing Room"},
        "Heavy coat pocket": {"emoji": "🧥", "tooltip": "Heavy coat pocket"},
        "Kitchen alibi": {"emoji": "🍳", "tooltip": "Has kitchen alibi"},
        "On site after 1 AM": {"emoji": "🌙", "tooltip": "On site after 1 AM"},
        "Has supervisor system access": {"emoji": "💻", "tooltip": "Supervisor system access"},
        "Fingerprint on canister": {"emoji": "👆", "tooltip": "Fingerprint on canister"},
        "Left before midnight": {"emoji": "⏰", "tooltip": "Left before midnight"},
        "Co-signed insurance": {"emoji": "📝", "tooltip": "Co-signed insurance"},
        "Delivered the whisky": {"emoji": "🥃", "tooltip": "Delivered the whisky"},
        "Named in new will": {"emoji": "📜", "tooltip": "Named in new will"},
        "Has chemistry knowledge": {"emoji": "🧪", "tooltip": "Has chemistry knowledge"},
        "Phone alibi in library": {"emoji": "📱", "tooltip": "Phone alibi in library"},
        "No motive found": {"emoji": "❓", "tooltip": "No motive found"},
    }
    
    # Get actual attributes from grid data
    attributes = grid_data["attributes"]
    
    # Create compact display names with emojis
    compact_attrs = []
    for attr in attributes:
        info = attribute_info.get(attr, {"emoji": "📌", "tooltip": attr})
        compact_attrs.append({
            "display": info["emoji"],
            "tooltip": info["tooltip"],
            "full": attr
        })

    st.markdown(f"""
        <div style='background:#0a1628;border:2px solid #3a6ea5;
            border-top:3px solid #e2c97e;border-radius:4px;
            padding:12px 16px;margin:16px 0;'>
        <p style='color:#e2c97e;font-family:"Special Elite",cursive;
            font-size:1rem;margin:0 0 4px 0;'>📊 LOGIC GRID</p>
        <p style='color:#94afc8;font-family:"Courier Prime",monospace;
            font-size:0.75rem;margin:0;'>{grid_data['intro']}</p>
        </div>
    """, unsafe_allow_html=True)

    suspects = grid_data["suspects"]
    
    # Initialize grid state
    if not st.session_state.logic_grid_state:
        st.session_state.logic_grid_state = {
            s: [False] * len(attributes) for s in suspects
        }

    # Create compact grid using columns
    st.markdown("---")
    
    # Header row with tooltips
    header_cols = st.columns([1.5] + [0.8] * len(attributes))
    header_cols[0].markdown("**SUSPECT**")
    for i, attr in enumerate(compact_attrs):
        with header_cols[i + 1]:
            st.markdown(
                f"<div title='{attr['tooltip']}' style='text-align:center; font-size:1.2rem; cursor:help;'>{attr['display']}</div>",
                unsafe_allow_html=True
            )
    
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    
    # Rows for each suspect
    for s in suspects:
        row_cols = st.columns([1.5] + [0.8] * len(attributes))
        row_cols[0].markdown(f"**{s}**")
        
        for i in range(len(attributes)):
            current = st.session_state.logic_grid_state[s][i]
            btn_label = "✅" if current else "⬜"
            with row_cols[i + 1]:
                if st.button(btn_label, key=f"grid_{s}_{i}", use_container_width=True):
                    st.session_state.logic_grid_state[s][i] = not current
                    st.rerun()
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("📤 Submit Grid", key="submit_grid", use_container_width=True):
            correct_map = grid_data["correct"]
            all_correct = True
            for s in suspects:
                player = st.session_state.logic_grid_state[s]
                expected = correct_map[s]
                if player != expected:
                    all_correct = False
                    break
            st.session_state.logic_grid_done = True
            st.session_state.logic_grid_result = "correct" if all_correct else "wrong"
            st.rerun()
    
    with col2:
        st.caption("💡 Hover over symbols to see what they mean!")

    return False

# ---------------------------
# SIDEBAR
# ---------------------------
with st.sidebar:
    st.markdown("## 🕵️ Detective Panel")
    difficulty = st.selectbox("Case Difficulty", ["easy", "medium", "hard"])
    st.markdown("---")
    st.markdown("### 📊 Mission Status")
    st.metric("🏆 Score", st.session_state.score)
    st.metric("🔁 Cases Solved", st.session_state.round - 1)
    elapsed = int(time.time() - st.session_state.start_time)
    minutes, seconds = divmod(elapsed, 60)
    st.metric("⏱️ Time", f"{minutes:02d}:{seconds:02d}")

    if st.session_state.step == 1 and st.session_state.case:
        st.markdown("---")
        st.markdown("### 💡 Hints")
        case_s = st.session_state.case
        hints = case_s.get("hints", [])
        used = st.session_state.hints_used
        remaining = len(hints) - used
        st.caption(f"{remaining} hint(s) remaining")
        if used < len(hints):
            if st.button("🔍 Use Hint (−3 pts)"):
                st.session_state.hints_used += 1
                st.session_state.score = max(0, st.session_state.score - 3)
                st.rerun()
        for i in range(used):
            st.info(f"💡 {hints[i]}")

        st.markdown("---")
        st.markdown("### 🧩 Puzzle Legend")
        if difficulty == "easy":
            st.markdown(
                "<p style='font-size:0.8rem;color:#94afc8;font-family:\"Courier Prime\",monospace;line-height:1.8;'>"
                "🔍 Easy mode: No puzzles — just investigate rooms!<br>"
                "✅ Green check = true evidence<br>"
                "⚠️ Red warning = misleading clue</p>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<p style='font-size:0.8rem;color:#94afc8;font-family:\"Courier Prime\",monospace;line-height:1.8;'>"
                "🔐 Red border = locked room<br>"
                "🧩 Amber border = riddle puzzle<br>"
                "🔢 Amber border = cipher puzzle (use helper!)<br>"
                "✅ Green = correct answer<br>"
                "⚠️ Red = misleading clue received<br>"
                "⏭️ Skip = −5 pts, true clue shown</p>",
                unsafe_allow_html=True
            )

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
            <h1 class='glow-amber' style='font-size:2.8rem; letter-spacing:3px;'>
                🕵️ CRIME SOLVER PRO
            </h1>
            <p style='color:#94afc8; font-size:1.1rem; letter-spacing:2px;'>
                DETECTIVE SYSTEM v4.0 — INITIALIZING...
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class='case-header fade-in'>
            <h3 style='margin-top:0'>📋 Mission Brief</h3>
            <ul style='color:#94afc8; line-height:2.2; font-family:"Courier Prime",monospace;'>
                <li>📂 Read the case file</li>
                <li>🗺️ Explore crime scene rooms to collect evidence</li>
                <li>📊 Fill out the logic grid as you discover facts (hover over symbols to see what they mean!)</li>
                <li>🔐 Solve puzzles in Medium/Hard mode to unlock evidence</li>
                <li>⚠️ Wrong answers give <strong>misleading clues</strong></li>
                <li>⏭️ Skip a puzzle for −5 pts (true clue revealed)</li>
                <li>⚖️ Accuse the correct culprit when ready</li>
            </ul>
            <p style='color:#e2c97e; margin-top:16px;'><strong>Easy mode:</strong> No puzzles — just investigate!</p>
            <p style='color:#e2c97e;'><strong>Medium/Hard mode:</strong> Use the Caesar cipher helper for coded messages!</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🟢 ENTER THE SYSTEM", use_container_width=True):
            st.session_state.started = True
            st.session_state.start_time = time.time()
            st.rerun()
    st.stop()

# ---------------------------
# CASE SELECTION
# ---------------------------
current_case = st.session_state.case
if (
    current_case is None
    or not current_case.get("rooms")
    or current_case.get("difficulty") != difficulty
):
    st.session_state.case = new_case(difficulty)
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
            <p style='color:#94afc8;font-size:0.8rem;letter-spacing:2px;margin:0 0 4px 0;'>
                CASE #{st.session_state.round:03d} — {case['difficulty'].upper()} — {env['location'].upper()}
            </p>
            <h2 style='margin:0 0 16px 0;'>📂 {case['title']}</h2>
            <p style='color:#c8d6e5;font-size:1.05rem;line-height:1.8;'>{case['story']}</p>
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

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔍 Begin Investigation →", use_container_width=True):
            st.session_state.start_time = time.time()
            st.session_state.step = 1
            st.rerun()

# ---------------------------
# STEP 1: Investigation + Logic Grid (Compact)
# ---------------------------
elif st.session_state.step == 1:
    step_bar(1, 3)
    st.markdown("## 🗺️ Crime Scene Investigation")
    st.caption("Investigate rooms to collect evidence. Tick the logic grid as you discover facts (hover over symbols to see what they mean)!")

    rooms = case["rooms"]
    visited = st.session_state.visited_rooms
    active = st.session_state.selected_room
    difficulty = case["difficulty"]

    # Two-column layout: Map on left, Logic Grid on right (more balanced)
    col_map, col_grid = st.columns([2, 1.2])

    with col_map:
        st.markdown("### 🗺️ Floor Plan")
        
        max_x = max(r["grid_x"] for r in rooms) + 1
        max_y = max(r["grid_y"] for r in rooms) + 1

        st.markdown(f"""
            <div style='background:#0a1628;border:2px solid #1e3a5f;
                border-top:3px solid #3a6ea5;border-radius:4px;
                padding:12px 16px 0 16px;'>
            <p style='color:#3a6ea5;font-size:0.7rem;letter-spacing:2px;margin:0 0 12px 0;'>
            ▪ FLOOR PLAN — {case["environment"]["location"].upper()} ▪
            </p>
        """, unsafe_allow_html=True)

        for y in range(max_y):
            cols = st.columns(max_x)
            for x in range(max_x):
                room = next((r for r in rooms if r["grid_x"] == x and r["grid_y"] == y), None)
                with cols[x]:
                    if room:
                        name = room["name"]
                        is_locked = room.get("locked", False) and name not in st.session_state.unlocked_rooms
                        is_active = (active == name)
                        is_visited = name in visited
                        clue_state = st.session_state.revealed_clues.get(name)

                        cell_class = "room-cell"
                        if is_active:
                            cell_class += " active"
                        elif is_visited:
                            cell_class += " visited"

                        badge = ""
                        if is_locked:
                            badge = "🔐 "
                        elif clue_state == "true":
                            badge = "✅ "
                        elif clue_state == "false":
                            badge = "⚠️ "
                        elif is_visited:
                            badge = "👁 "

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
                                45deg,#090f1a,#090f1a 6px,#0b1220 6px,#0b1220 12px);
                                border:1px solid #0f1e30;border-radius:2px;min-height:90px;'>
                            </div>
                        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Room Detail Panel
        st.markdown("### 🔍 Current Location")
        if active:
            room_data = next((r for r in rooms if r["name"] == active), None)
            if room_data:
                is_locked = room_data.get("locked", False)
                if is_locked:
                    unlocked = render_lock(room_data)
                    if not unlocked:
                        st.stop()

                col_img, col_info = st.columns([2, 3])
                with col_img:
                    img = room_data.get("image_url", "")
                    if img and img != "YOUR_PHOTO_HERE":
                        st.image(img, caption=f"📷 {room_data['name']}", use_container_width=True)
                    else:
                        st.markdown(f"""
                            <div style='background:#0f1e30;border:2px dashed #1e3a5f;
                                border-radius:4px;height:200px;display:flex;
                                align-items:center;justify-content:center;'>
                            <span style='font-size:3rem;'>{room_data['icon']}</span>
                            </div>
                        """, unsafe_allow_html=True)

                with col_info:
                    st.markdown(f"### {room_data['icon']} {room_data['name']}")
                    info_box(room_data["description"])
                    st.markdown(f"""
                        <div style='background:#1f180a;border:1px solid #e2c97e;
                            border-radius:2px;padding:8px 14px;margin:8px 0;
                            color:#e2c97e;font-size:0.88rem;
                            font-family:"Courier Prime",monospace;'>
                        🔍 Object: <strong>{room_data['object']}</strong>
                        </div>
                    """, unsafe_allow_html=True)

                    render_puzzle(room_data, difficulty)

                if "suspect" in room_data:
                    sname = room_data["suspect"]
                    sinfo = case["suspects"].get(sname)
                    if sinfo:
                        st.markdown(f"""
                            <div class='suspect-card' style='background:#0a1628;border-left:3px solid #e2c97e;padding:12px;margin:12px 0;'>
                                <strong>👤 {sname}</strong> — {sinfo['description']}
                                <blockquote style='color:#94afc8;margin-top:8px;'>"{random.choice(sinfo['dialogue'])}"</blockquote>
                            </div>
                        """, unsafe_allow_html=True)

                st.markdown("---")
                
                if st.button("⚖️ Ready to Accuse?", use_container_width=True, type="primary"):
                    st.session_state.step = 2
                    st.rerun()
        else:
            st.info("👆 Click **Enter** beneath any room on the blueprint to investigate.")

        # Progress stats
        st.markdown("<br>", unsafe_allow_html=True)
        visited_count = len(st.session_state.visited_rooms)
        true_clues = sum(1 for v in st.session_state.revealed_clues.values() if v == "true")
        false_clues = sum(1 for v in st.session_state.revealed_clues.values() if v == "false")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🚪 Rooms Visited", f"{visited_count}/{len(rooms)}")
        c2.metric("✅ True Clues", true_clues)
        c3.metric("⚠️ False Clues", false_clues)
        c4.metric("💡 Hints Used", st.session_state.hints_used)

    with col_grid:
        st.markdown("### 📊 Logic Grid")
        st.caption("Hover over symbols to see what they mean!")
        render_logic_grid(case)

# ---------------------------
# STEP 2: Verdict
# ---------------------------
elif st.session_state.step == 2:
    step_bar(2, 3)
    correct = case["answer"]

    st.markdown("## ⚖️ Make Your Accusation")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 🧑 Suspects")
        suspect_options = list(case["suspects"].keys())
        selected = st.radio(
            "Select the guilty suspect:",
            suspect_options,
            key="final_accusation"
        )

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
        true_clues = sum(1 for v in st.session_state.revealed_clues.values() if v == "true")
        false_clues = sum(1 for v in st.session_state.revealed_clues.values() if v == "false")

        info_box(f"""
        **Rooms investigated:** {visited_count}/{len(case['rooms'])}<br>
        **True clues found:** {true_clues}<br>
        **Misleading clues:** {false_clues}<br>
        **Hints used:** {st.session_state.hints_used}<br>
        **Logic grid:** {st.session_state.logic_grid_result or "Not submitted"}
        """)

        false_rooms = [r for r, v in st.session_state.revealed_clues.items() if v == "false"]
        if false_rooms:
            st.warning(f"⚠️ Be careful — you received misleading clues in: {', '.join(false_rooms)}")

# ---------------------------
# STEP 3: Verdict Result
# ---------------------------
elif st.session_state.step == 3:
    step_bar(3, 3)
    correct = case["answer"]
    selected = st.session_state.selected_suspect
    time_taken = int(time.time() - st.session_state.start_time)
    minutes, seconds = divmod(time_taken, 60)
    is_correct = (selected == correct)

    false_count = sum(1 for v in st.session_state.revealed_clues.values() if v == "false")

    if is_correct:
        speed_bonus = max(60 - time_taken, 0)
        hint_penalty = st.session_state.hints_used * 3
        false_penalty = false_count * 5
        points = max(case.get("reward_points", 10) + speed_bonus - hint_penalty - false_penalty, 1)
        st.session_state.score += points

        st.markdown(f"""
            <div class='verdict-correct fade-in'>
                <h2 class='glow'>✔ CASE CLOSED</h2>
                <p style='color:#c8d6e5;font-size:1.1rem;'>
                    Correct. <strong>{correct}</strong> is the culprit.
                </p>
                <p style='color:#22c55e;font-size:1.4rem;font-weight:bold;'>+{points} points</p>
                <p style='color:#94afc8;font-size:0.85rem;'>
                    Base: {case['reward_points']} | Speed: +{speed_bonus} |
                    Hints: −{hint_penalty} | Misleads followed: −{false_penalty}
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class='verdict-wrong fade-in'>
                <h2 style='color:#ef4444;'>✗ WRONG ACCUSATION</h2>
                <p style='color:#c8d6e5;font-size:1.1rem;'>
                    You accused <strong>{selected}</strong>.
                    The real culprit was <strong>{correct}</strong>.
                </p>
                <p style='color:#ef4444;'>No points awarded.</p>
                {f"<p style='color:#94afc8;font-size:0.85rem;'>You followed {false_count} misleading clue(s). That may have cost you.</p>" if false_count else ""}
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
                text = rd["clue_revealed"] if was_correct else rd.get("false_clue", rd.get("puzzle", {}).get("false_clue", "Misleading clue."))
                clue_box(f"{rd['icon']} <strong>{rname}:</strong> {text}", correct=was_correct)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📁 Next Case →", use_container_width=True):
        st.session_state.round += 1
        st.session_state.step = 0
        st.session_state.case = new_case(difficulty, exclude=case)
        reset_investigation()
        st.rerun()