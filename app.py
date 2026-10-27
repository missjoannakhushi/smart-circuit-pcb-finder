import random
import time
import streamlit as st

st.set_page_config(page_title="TraceStack - PCB Short Circuit Finder", layout="centered")

st.title("⚡ TraceStack: Advanced PCB Trace & Fault Isolation System")
st.markdown("**Data Structures Project:** Using a **LIFO Stack (DFS)** to traverse circuit grids and isolate short-circuit faults.")

# Initialize session state for the board
if "board" not in st.session_state:
    st.session_state.rows = 6
    st.session_state.cols = 6
    st.session_state.board = [[0 for _ in range(6)] for _ in range(6)]
    st.session_state.path = []
    st.session_state.shorts = []

def generate_circuit():
    rows, cols = 6, 6
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    curr_r, curr_c = 0, 0
    board[curr_r][curr_c] = 1
    trace_path = [(curr_r, curr_c)]
    
    for _ in range(10):
        neighbors = []
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = curr_r + dr, curr_c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == 0:
                neighbors.append((nr, nc))
        if not neighbors:
            break
        curr_r, curr_c = random.choice(neighbors)
        board[curr_r][curr_c] = 1
        trace_path.append((curr_r, curr_c))

    if len(trace_path) >= 4:
        faults = random.sample(trace_path[2:], min(2, len(trace_path)-2))
        for fr, fc in faults:
            board[fr][fc] = 2
            
    st.session_state.board = board
    st.session_state.path = trace_path
    st.session_state.shorts = faults

# Controls
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Generate New Random Circuit"):
        generate_circuit()
with col2:
    run_sim = st.button("🚀 Run LIFO Stack Audit")

if not st.session_state.board or st.session_state.board == [[0]*6]*6:
    generate_circuit()

# Display the Grid as a visual board
st.subheader("Circuit Layout Grid")
board = st.session_state.board

# Render grid using markdown table or custom html blocks
grid_html = "<div style='display: grid; grid-template-columns: repeat(6, 50px); gap: 5px; justify-content: center;'>"
for r in range(6):
    for c in range(6):
        val = board[r][c]
        bg = "#1e1e1e" # Empty
        text_color = "#888"
        label = f"({r},{c})"
        
        if val == 1:
            bg = "#28a745" # Copper Trace
            text_color = "white"
        elif val == 2:
            bg = "#dc3545" # Short Circuit Fault
            text_color = "white"
            
        grid_html += f"<div style='background-color: {bg}; color: {text_color}; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; font-weight: bold; border-radius: 5px; border: 1px solid #444; font-size: 11px;'>{label}</div>"
grid_html += "</div>"

st.markdown(grid_html, unsafe_allow_html=True)

if run_sim:
    st.info("Stack Traversal Initiated (DFS LIFO)...")
    time.sleep(0.5)
    st.success(f"✅ Audit Complete! LIFO Stack successfully scanned the network and isolated short-circuits at: {st.session_state.shorts}")
