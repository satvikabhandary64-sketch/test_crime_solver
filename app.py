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
    "revealed_clues": [],
    "hints_used": 0,
    "accusation_suspect": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------------------
# HELPERS
# ---------------------------
def step_bar(current: int, total: int = 4):
    dots = ""
    for i in range(total):
        if i < current:
            cls = "done"
        elif i == current:
            cls = "active"
        else:
            cls = ""
        dots += f'<div class="step-dot {cls}"></div>'
    labels = ["📂 Case File", "🧾 Evidence", "🗺️ Investigate", "⚖️ Verdict"]
    st.markdown(
        f'<div class="step-bar">{dots}</div>'
        f'<p style="font-size:0.75rem;color:#94afc8;margin:0 0 16px 0;">'
        f'Step {current+1}/4 — {labels[min(current, 3)]}</p>',
        unsafe_allow_html=True
    )

def new_case(difficulty: str, exclude=None):
    pool = [c for c in cases if c["difficulty"] == difficulty]
    if exclude and len(pool) > 1:
        pool = [c for c in pool if c != exclude]
    return random.choice(pool)

def reset_investigation():
    st.session_state.selected_room = None
    st.session_state.visited_rooms = []
    st.session_state.revealed_clues = []
    st.session_state.hints_used = 0
    st.session_state.accusation_suspect = None
    st.session_state.selected_suspect = ""
    st.session_state.reasoning = ""

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

    if st.session_state.step == 2 and st.session_state.case:
        st.markdown("---")
        st.markdown("### 💡 Hints")
        case = st.session_state.case
        hints = case.get("hints", [])
        used = st.session_state.hints_used
        remaining = len(hints) - used
        st.caption(f"{remaining} hint(s) remaining")
        if used < len(hints):
            if st.button("🔍 Use a Hint (-3 pts)"):
                st.session_state.hints_used += 1
                st.session_state.score = max(0, st.session_state.score - 3)
                st.rerun()
        for i in range(used):
            st.info(f"💡 {hints[i]}")

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
                DETECTIVE SYSTEM v2.0 — INITIALIZING...
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class='case-header fade-in'>
            <h3 style='margin-top:0'>📋 Mission Brief</h3>
            <p>You are Detective. Your task:</p>
            <ul style='color:#94afc8; line-height:2;'>
                <li>📂 Read the case file carefully</li>
                <li>🧾 Study the evidence board</li>
                <li>🗺️ Explore the crime scene room by room</li>
                <li>🔎 Reveal clues hidden in each location</li>
                <li>💬 Hear what suspects have to say</li>
                <li>⚖️ Accuse the correct culprit</li>
                <li>⚡ Faster solutions earn more points</li>
            </ul>
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
if st.session_state.case is None:
    st.session_state.case = new_case(difficulty)
    reset_investigation()

case = st.session_state.case

# ---------------------------
# STEP 0: Case File
# ---------------------------
if st.session_state.step == 0:
    step_bar(0)
    st.markdown(f"""
        <div class='case-header fade-in'>
            <p style='color:#94afc8; font-size:0.8rem; letter-spacing:2px; margin:0 0 4px 0;'>
                CASE #{st.session_state.round:03d} — {case['difficulty'].upper()} — {case['environment']['location'].upper()}
            </p>
            <h2 style='margin:0 0 16px 0;'>📂 {case['title']}</h2>
            <p style='color:#c8d6e5; font-size:1.05rem; line-height:1.8;'>{case['story']}</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    env = case["environment"]
    with col1:
        st.markdown(f"**📍 Location:** {env['location']}")
        st.markdown(f"**🕐 Time:** {env['time']}")
    with col2:
        st.markdown(f"**🌧️ Weather:** {env['weather']}")
        st.markdown(f"**🔊 Sounds:** {env['sounds']}")
    with col3:
        suspect_names = ", ".join(case["suspects"].keys())
        st.markdown(f"**🧑‍🤝‍🧑 Suspects:** {suspect_names}")
        st.markdown(f"**🏆 Reward:** {case['reward_points']} base pts")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔍 Begin Investigation →", use_container_width=True):
        st.session_state.start_time = time.time()
        st.session_state.step = 1
        st.rerun()

# ---------------------------
# STEP 1: Evidence Board
# ---------------------------
elif st.session_state.step == 1:
    step_bar(1)
    st.markdown("## 🧾 Evidence Board")
    st.caption("Study all clues before entering the crime scene.")

    col_clues, col_suspects = st.columns([3, 2])

    with col_clues:
        st.markdown("### 🔎 Known Clues")
        for i, clue in enumerate(case["clues"]):
            st.markdown(f"""
                <div style='
                    background:#0f1e30; border:1px solid #1e3a5f;
                    border-left:3px solid #e2c97e; border-radius:2px;
                    padding:10px 14px; margin:6px 0;
                    font-family:"Courier Prime",monospace; color:#c8d6e5;
                '>
                🔎 {clue}
                </div>
            """, unsafe_allow_html=True)

    with col_suspects:
        st.markdown("### 🧑 Known Suspects")
        for name, info in case["suspects"].items():
            with st.expander(f"👤 {name}"):
                st.markdown(f"*{info['description']}*")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗺️ Enter Crime Scene →", use_container_width=True):
        st.session_state.step = 2
        st.rerun()

# ---------------------------
# STEP 2: Blueprint Map Investigation
# ---------------------------
elif st.session_state.step == 2:
    step_bar(2)
    st.markdown("## 🗺️ Crime Scene Investigation")
    st.caption("Click a room on the blueprint to investigate. Gather evidence, then accuse a suspect.")

    rooms = case["rooms"]
    visited = st.session_state.visited_rooms
    active = st.session_state.selected_room

    # ---- Build 2D grid ----
    max_x = max(r["grid_x"] for r in rooms) + 1
    max_y = max(r["grid_y"] for r in rooms) + 1

    # Grid header label
    st.markdown("""
        <div style='
            background:#0a1628;
            border:2px solid #1e3a5f;
            border-top:3px solid #3a6ea5;
            border-radius:4px;
            padding:12px 16px 0 16px;
            margin-bottom:0;
            position:relative;
        '>
        <p style='color:#3a6ea5;font-size:0.7rem;letter-spacing:2px;margin:0 0 12px 0;'>
            ▪ FLOOR PLAN — {loc} ▪
        </p>
    """.format(loc=case["environment"]["location"].upper()), unsafe_allow_html=True)

    # Render grid rows
    for y in range(max_y):
        cols = st.columns(max_x)
        for x in range(max_x):
            room = next((r for r in rooms if r["grid_x"] == x and r["grid_y"] == y), None)
            with cols[x]:
                if room:
                    name = room["name"]
                    icon = room["icon"]
                    is_active = (active == name)
                    is_visited = name in visited

                    cell_class = "room-cell"
                    if is_active:
                        cell_class += " active"
                    elif is_visited:
                        cell_class += " visited"

                    badge = "✅ " if is_visited and not is_active else ""

                    st.markdown(f"""
                        <div class='{cell_class}'>
                            <span class='room-icon'>{icon}</span>
                            <span class='room-name'>{badge}{name}</span>
                        </div>
                    """, unsafe_allow_html=True)

                    if st.button(f"Enter", key=f"room_{x}_{y}"):
                        st.session_state.selected_room = name
                        if name not in st.session_state.visited_rooms:
                            st.session_state.visited_rooms.append(name)
                        st.rerun()
                else:
                    # Empty cell — hallway / wall gap
                    st.markdown("""
                        <div style='
                            background:repeating-linear-gradient(
                                45deg,
                                #090f1a,
                                #090f1a 6px,
                                #0b1220 6px,
                                #0b1220 12px
                            );
                            border:1px solid #0f1e30;
                            border-radius:2px;
                            min-height:90px;
                        '></div>
                    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close blueprint container
    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Room Detail Panel ----
    if active:
        room_data = next((r for r in rooms if r["name"] == active), None)
        if room_data:
            col_img, col_info = st.columns([2, 3])

            with col_img:
                st.image(
                    room_data["image_url"],
                    caption=f"📷 {room_data['name']}",
                    use_container_width=True
                )

            with col_info:
                st.markdown(f"### {room_data['icon']} {room_data['name']}")
                st.markdown(f"""
                    <div style='
                        background:#0f1e30; border:1px solid #1e3a5f;
                        border-radius:2px; padding:12px 16px; margin-bottom:12px;
                        color:#c8d6e5; font-family:"Courier Prime",monospace;
                        line-height:1.7;
                    '>
                    {room_data['description']}
                    </div>
                """, unsafe_allow_html=True)

                # Object found
                st.markdown(f"""
                    <div style='
                        background:#1f180a; border:1px solid #e2c97e;
                        border-radius:2px; padding:8px 14px; margin-bottom:12px;
                        color:#e2c97e; font-size:0.88rem;
                        font-family:"Courier Prime",monospace;
                    '>
                    🔍 Object: <strong>{room_data['object']}</strong>
                    </div>
                """, unsafe_allow_html=True)

                # Revealed clue
                clue_key = f"clue_{active}"
                if clue_key not in st.session_state.revealed_clues:
                    if st.button("🔦 Examine Evidence", key="examine"):
                        st.session_state.revealed_clues.append(clue_key)
                        st.rerun()
                else:
                    st.markdown(f"""
                        <div style='
                            background:#0a1628; border:1px solid #3a6ea5;
                            border-left:4px solid #22c55e; border-radius:2px;
                            padding:10px 14px; color:#22c55e;
                            font-family:"Courier Prime",monospace; font-size:0.9rem;
                        '>
                        📋 Clue revealed: {room_data['clue_revealed']}
                        </div>
                    """, unsafe_allow_html=True)

            # Suspect dialogue (if room has a linked suspect)
            if "suspect" in room_data:
                suspect_name = room_data["suspect"]
                suspect_info = case["suspects"].get(suspect_name)
                if suspect_info:
                    st.markdown(f"""
                        <div class='suspect-card'>
                            <strong>👤 {suspect_name}</strong> — {suspect_info['description']}
                            <blockquote>
                                "{random.choice(suspect_info['dialogue'])}"
                            </blockquote>
                        </div>
                    """, unsafe_allow_html=True)

                    # Interrogate button
                    interrogate_key = f"interrogate_{active}"
                    if st.button(f"🎙️ Interrogate {suspect_name}", key=interrogate_key):
                        st.session_state[f"extra_dialogue_{suspect_name}"] = random.choice(
                            suspect_info["dialogue"]
                        )
                        st.rerun()

                    extra = st.session_state.get(f"extra_dialogue_{suspect_name}")
                    if extra:
                        st.info(f'💬 {suspect_name}: "{extra}"')

            st.markdown("---")

            # Accuse from this room
            st.markdown("### ⚖️ Ready to Accuse?")
            suspect_options = list(case["suspects"].keys())
            accusation = st.selectbox(
                "Select suspect to accuse",
                ["-- Select --"] + suspect_options,
                key="accusation_select"
            )
            reasoning_input = st.text_area(
                "Your reasoning (optional)",
                placeholder="Explain why you think this suspect is guilty...",
                key="reasoning_input",
                height=80
            )

            rooms_visited = len(visited)
            rooms_total = len(rooms)
            st.caption(f"Rooms investigated: {rooms_visited}/{rooms_total}")

            if rooms_visited < 2:
                st.warning("⚠️ Investigate at least 2 rooms before making an accusation.")
            elif accusation != "-- Select --":
                if st.button(f"🎯 ACCUSE {accusation.upper()}", use_container_width=True):
                    st.session_state.selected_suspect = accusation
                    st.session_state.reasoning = reasoning_input or f"Accused from {active}."
                    st.session_state.step = 3
                    st.rerun()

    else:
        st.info("👆 Click **Enter** beneath any room on the blueprint to start investigating.")

    # Progress summary
    st.markdown("<br>", unsafe_allow_html=True)
    visited_count = len(st.session_state.visited_rooms)
    total_rooms = len(rooms)
    revealed_count = len(st.session_state.revealed_clues)

    c1, c2, c3 = st.columns(3)
    c1.metric("🚪 Rooms Visited", f"{visited_count}/{total_rooms}")
    c2.metric("🔎 Clues Revealed", revealed_count)
    c3.metric("💡 Hints Used", st.session_state.hints_used)

# ---------------------------
# STEP 3: Verdict
# ---------------------------
elif st.session_state.step == 3:
    step_bar(3)
    correct = case["answer"]
    selected = st.session_state.selected_suspect
    time_taken = int(time.time() - st.session_state.start_time)
    minutes, seconds = divmod(time_taken, 60)

    is_correct = (selected == correct)

    if is_correct:
        speed_bonus = max(60 - time_taken, 0)
        hint_penalty = st.session_state.hints_used * 3
        points = case.get("reward_points", 10) + speed_bonus - hint_penalty
        points = max(points, 1)
        st.session_state.score += points

        st.markdown(f"""
            <div class='verdict-correct fade-in'>
                <h2 class='glow'>✔ CASE CLOSED</h2>
                <p style='color:#c8d6e5; font-size:1.1rem;'>
                    Your accusation was correct. <strong>{correct}</strong> is the culprit.
                </p>
                <p style='color:#22c55e; font-size:1.4rem; font-weight:bold;'>
                    +{points} points earned
                </p>
                <p style='color:#94afc8; font-size:0.85rem;'>
                    Base: {case['reward_points']} | Speed bonus: +{speed_bonus} | Hints: -{hint_penalty}
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class='verdict-wrong fade-in'>
                <h2 style='color:#ef4444;'>✗ WRONG ACCUSATION</h2>
                <p style='color:#c8d6e5; font-size:1.1rem;'>
                    You accused <strong>{selected}</strong>, but the real culprit was <strong>{correct}</strong>.
                </p>
                <p style='color:#ef4444;'>No points awarded.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🧠 Case Explanation")
        st.markdown(f"""
            <div style='
                background:#0f1e30; border:1px solid #1e3a5f;
                border-left:4px solid #e2c97e; border-radius:2px;
                padding:14px 18px; color:#c8d6e5;
                font-family:"Courier Prime",monospace; line-height:1.8;
            '>
            {case.get('explanation', 'No explanation available.')}
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 📋 Your Investigation")
        st.markdown(f"""
            <div style='
                background:#0f1e30; border:1px solid #1e3a5f;
                border-radius:2px; padding:14px 18px;
                font-family:"Courier Prime",monospace;
            '>
            <p style='color:#94afc8; margin:0 0 6px 0;'>⏱️ Time: {minutes:02d}:{seconds:02d}</p>
            <p style='color:#94afc8; margin:0 0 6px 0;'>🚪 Rooms visited: {len(st.session_state.visited_rooms)}/{len(case['rooms'])}</p>
            <p style='color:#94afc8; margin:0 0 6px 0;'>🔎 Clues revealed: {len(st.session_state.revealed_clues)}</p>
            <p style='color:#94afc8; margin:0 0 12px 0;'>💡 Hints used: {st.session_state.hints_used}</p>
            <p style='color:#c8d6e5; font-style:italic; margin:0;'>"{st.session_state.reasoning}"</p>
            </div>
        """, unsafe_allow_html=True)

    # Visited rooms recap
    st.markdown("### 🗺️ Rooms You Investigated")
    visited_names = st.session_state.visited_rooms
    if visited_names:
        cols = st.columns(min(len(visited_names), 3))
        for i, rname in enumerate(visited_names):
            rd = next((r for r in case["rooms"] if r["name"] == rname), None)
            if rd:
                with cols[i % 3]:
                    st.markdown(f"""
                        <div style='
                            background:#0f1e30; border:1px solid #1e3a5f;
                            border-radius:2px; padding:10px; text-align:center;
                            font-family:"Courier Prime",monospace;
                        '>
                        <span style='font-size:1.4rem;'>{rd['icon']}</span><br>
                        <span style='color:#94afc8; font-size:0.8rem;'>{rname}</span>
                        </div>
                    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📁 Next Case →", use_container_width=True):
        st.session_state.round += 1
        st.session_state.step = 0
        st.session_state.case = new_case(difficulty, exclude=case)
        reset_investigation()
        st.rerun()