import streamlit as st
import pandas as pd
import pydeck as pdk
import random
import time
from cases import cases

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Crime Solver Pro", page_icon="🕵️")

# ---------------------------
# LOAD CSS
# ---------------------------
def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass  # Skip if no CSS file

load_css()

# ---------------------------
# SESSION STATE INIT
# ---------------------------
if "started" not in st.session_state:
    st.session_state.started = False
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.round = 1
    st.session_state.start_time = time.time()
    st.session_state.step = 0
    st.session_state.case = None
    st.session_state.selected = ""
    st.session_state.reasoning = ""

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("🕵️ Detective Panel")
difficulty = st.sidebar.selectbox("Case Difficulty", ["easy", "medium", "hard"])
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Status")
st.sidebar.write(f"🏆 Score: {st.session_state.score}")
st.sidebar.write(f"🔁 Cases Solved: {st.session_state.round}")
elapsed_time = int(time.time() - st.session_state.start_time)
st.sidebar.write(f"⏱️ Time: {elapsed_time}s")

# ---------------------------
# LANDING PAGE
# ---------------------------
if not st.session_state.started:
    st.markdown("""
        <h1 class='typewriter glow' style='text-align:center;'>🕵️ Crime Solver System Initializing...</h1>
    """, unsafe_allow_html=True)
    time.sleep(0.5)
    st.markdown("""
        <div class='fade-in'>
        <h3 style='text-align:center;'>Access Granted</h3>
        <p style='text-align:center;'>Welcome Detective. Analyze evidence, interrogate suspects, and solve the case.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("🟢 ENTER SYSTEM"):
            st.session_state.started = True
            st.rerun()

    st.markdown("---")
    st.markdown("### 🧾 Mission Brief")
    st.write("""
    - Analyze clues carefully  
    - Inspect objects at the crime scene  
    - Interrogate suspects  
    - Make the correct accusation  
    - Solve cases quickly for higher score  
    """)
    st.stop()

# ---------------------------
# CASE SELECTION
# ---------------------------
filtered_cases = [c for c in cases if c["difficulty"] == difficulty]
if st.session_state.case is None:
    st.session_state.case = random.choice(filtered_cases)

case = st.session_state.case

# ---------------------------
# GAME LOGIC
# ---------------------------

# STEP 0: Case File
if st.session_state.step == 0:
    st.subheader("📂 Case File")
    st.markdown(f"### {case['title'].title()}")
    st.write(case["story"])
    if st.button("🔍 Begin Investigation"):
        st.session_state.start_time = time.time()
        st.session_state.step = 1
        st.rerun()

# STEP 1: Evidence Board
elif st.session_state.step == 1:
    st.subheader("🧾 Evidence Board")
    for clue in case["clues"]:
        st.markdown(f'🔎 {clue}')
    
    # Inspect objects
    st.markdown("### 🕵️ Crime Scene Objects")
    objects = {obj["name"]: obj["description"] for obj in case.get("objects", [])}
    if objects:
        selected_object = st.selectbox("Inspect Object", ["--Select--"] + list(objects.keys()))
        if selected_object != "--Select--":
            st.info(objects[selected_object])
    
    if st.button("➡️ Analyze Suspects"):
        st.session_state.step = 2
        st.rerun()

# STEP 2: Interactive Map Investigation
elif st.session_state.step == 2:
    st.subheader("🗺️ Crime Scene Investigation")

    # -----------------------
    # Define locations on the map
    # Each location has: name, lat/lon (or arbitrary coordinates), suspect, object, icon
    # -----------------------
    # Example coordinates (arbitrary 2D plane)
    crime_scene_locations = pd.DataFrame([
        {"name": "Kitchen", "x": 1, "y": 5, "suspect": "Alice", "object": "Knife", "icon": "🥄"},
        {"name": "Living Room", "x": 3, "y": 7, "suspect": "Bob", "object": "Wallet", "icon": "🛋️"},
        {"name": "Bedroom", "x": 5, "y": 2, "suspect": "Clara", "object": "Necklace", "icon": "🛏️"},
        {"name": "Garage", "x": 7, "y": 4, "suspect": "David", "object": "Toolbox", "icon": "🔧"},
        {"name": "Garden", "x": 2, "y": 1, "suspect": "Eve", "object": "Flower Pot", "icon": "🌷"},
    ])

    # -----------------------
    # Store selected location
    # -----------------------
    if "selected_location" not in st.session_state:
        st.session_state.selected_location = None

    # -----------------------
    # Display locations as clickable buttons
    # -----------------------
    st.markdown("### 🔍 Explore the Crime Scene")
    for idx, loc in crime_scene_locations.iterrows():
        cols = st.columns([1, 4, 1])
        with cols[1]:
            if st.button(f"{loc['icon']} {loc['name']}", key=f"loc_{idx}"):
                st.session_state.selected_location = loc["name"]

    # -----------------------
    # Inspect selected location
    # -----------------------
    if st.session_state.selected_location:
        loc_info = crime_scene_locations[crime_scene_locations["name"] == st.session_state.selected_location].iloc[0]
        st.markdown(f"### 🕵️ You are at: {loc_info['name']}")
        
        # Show object
        st.info(f"Object found here: {loc_info['object']}")
        
        # Show suspect dialogue (from your cases)
        suspect_name = loc_info["suspect"]
        suspect_dialogue = case["suspects"].get(suspect_name, {"dialogue": ["No one here."]}).get("dialogue", ["No one here."])
        dialogue_line = random.choice(suspect_dialogue)
        st.success(f"Suspect {suspect_name} says: {dialogue_line}")

        # Allow player to make this location their guess
        if st.button("🎯 Accuse suspect here"):
            st.session_state.selected = suspect_name
            st.session_state.reasoning = f"Player visited {loc_info['name']} and inspected {loc_info['object']}."
            st.session_state.step = 3
            st.rerun()
            
# STEP 3: Verdict
elif st.session_state.step == 3:
    st.subheader("⚖️ Verdict")
    correct = case["answer"]
    selected = st.session_state.selected
    time_taken = int(time.time() - st.session_state.start_time)
    
    if selected == correct:
        st.success("✅ Case Solved!")
        st.markdown("<h2 class='glow'>✔ CASE CLOSED</h2>", unsafe_allow_html=True)
        points = case.get("reward_points", 10) + max(50 - time_taken, 0)
        st.session_state.score += points
        st.info(f"Points earned: {points}")
    else:
        st.error(f"❌ Wrong Accusation! Culprit: {correct}")
    
    st.markdown("### 🧠 Your Reasoning")
    st.write(st.session_state.reasoning)
    
    if st.button("📁 Next Case"):
        st.session_state.round += 1
        st.session_state.step = 0
        remaining_cases = [c for c in filtered_cases if c != case]
        st.session_state.case = random.choice(remaining_cases) if remaining_cases else random.choice(filtered_cases)
        st.session_state.selected = ""
        st.session_state.reasoning = ""
        st.session_state.start_time = time.time()
        st.rerun()