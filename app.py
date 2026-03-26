import streamlit as st
from cases import cases
import random

st.set_page_config(page_title="Crime Case Solver", page_icon="🕵️")

st.title("🕵️ Crime Case Solver")

# Initialize session state
if "case" not in st.session_state:
    st.session_state.case = random.choice(cases)
    st.session_state.step = 0
    st.session_state.selected_suspect = None

case = st.session_state.case

# Step 1: Show story
if st.session_state.step == 0:
    st.header(case["title"])
    st.write(case["story"])
    
    if st.button("Start Investigation"):
        st.session_state.step = 1

# Step 2: Show clues
elif st.session_state.step == 1:
    st.subheader("🔍 Clues")
    
    for clue in case["clues"]:
        st.write(f"- {clue}")
    
    if st.button("View Suspects"):
        st.session_state.step = 2

# Step 3: Show suspects
elif st.session_state.step == 2:
    st.subheader("🧑 Suspects")
    
    for suspect, desc in case["suspects"].items():
        st.write(f"**{suspect}**: {desc}")
    
    st.session_state.selected_suspect = st.selectbox(
        "Who is the culprit?",
        list(case["suspects"].keys())
    )
    
    if st.button("Submit Answer"):
        st.session_state.step = 3

# Step 4: Result
elif st.session_state.step == 3:
    correct = case["answer"]
    selected = st.session_state.selected_suspect
    
    if selected == correct:
        st.success(f"✅ Correct! {correct} is the culprit.")
    else:
        st.error(f"❌ Wrong! The correct answer was {correct}.")
    
    if st.button("Play Again"):
        st.session_state.case = random.choice(cases)
        st.session_state.step = 0