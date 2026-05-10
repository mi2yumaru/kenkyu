#!/usr/bin/env python3
"""
Avida Live Visualizer
リアルタイムでAvida シミュレーションの出力をグラフ表示する
スレッド安全な設計：スレッドは queue に入れるだけ、メインはそれを処理
"""

import streamlit as st
import subprocess
import threading
import queue
import re
from collections import deque
import matplotlib.pyplot as plt
from datetime import datetime

# ========================================
# ページ設定
# ========================================
st.set_page_config(page_title="Avida Live Visualizer", layout="wide")
st.title("🧬 Avida Live Visualizer")


# ========================================
# Session State 初期化（メインスレッド開始時）
# ========================================
def initialize_session_state():
    """Initialize all required session_state variables."""
    if "data_queue" not in st.session_state:
        st.session_state.data_queue = queue.Queue()
    if "raw_lines" not in st.session_state:
        st.session_state.raw_lines = deque(maxlen=100)
    if "stderr_lines" not in st.session_state:
        st.session_state.stderr_lines = deque(maxlen=20)
    if "parsed_rows" not in st.session_state:
        st.session_state.parsed_rows = deque(maxlen=1000)
    if "parse_success" not in st.session_state:
        st.session_state.parse_success = 0
    if "parse_fail" not in st.session_state:
        st.session_state.parse_fail = 0
    if "last_parsed" not in st.session_state:
        st.session_state.last_parsed = None
    if "last_raw_line" not in st.session_state:
        st.session_state.last_raw_line = ""
    if "process_started" not in st.session_state:
        st.session_state.process_started = False
    if "running" not in st.session_state:
        st.session_state.running = False
    if "worker_thread" not in st.session_state:
        st.session_state.worker_thread = None
    if "process_pid" not in st.session_state:
        st.session_state.process_pid = None
    if "process_exit_code" not in st.session_state:
        st.session_state.process_exit_code = None
    if "stdout_lines_received" not in st.session_state:
        st.session_state.stdout_lines_received = 0
    if "queue_items_received" not in st.session_state:
        st.session_state.queue_items_received = 0
    if "avida_exe_path" not in st.session_state:
        st.session_state.avida_exe_path = "C:\\avida\\build\\bin\\Debug\\avida.exe"
    if "avida_cwd" not in st.session_state:
        st.session_state.avida_cwd = "C:\\avida\\build\\bin\\Debug"


# ========================================
# パース関数
# ========================================
def parse_avida_line(line):
    """
    Parse Avida output line format:
    UD: 752   Gen: 57.83987   Fit: 0.2486994   Orgs: 3597
    
    Returns dict with parsed values or None if parse fails.
    """
    pattern = r'UD:\s*([\d.]+)\s+Gen:\s*([\d.]+)\s+Fit:\s*([\d.]+)\s+Orgs:\s*([\d]+)'
    match = re.search(pattern, line)
    
    if match:
        try:
            return {
                "ud": float(match.group(1)),
                "gen": float(match.group(2)),
                "fit": float(match.group(3)),
                "orgs": int(match.group(4))
            }
        except (ValueError, IndexError):
            return None
    return None




# ========================================
# バックグラウンドスレッド関数
# （Streamlit API を一切使用しない）
# ========================================
def run_avida_simulation(queue_obj):
    """
    Run Avida simulation and send data through queue.
    This function runs in a background thread and MUST NOT touch st.session_state or st.* APIs.
    """
    avida_exe = "C:\\avida\\build\\bin\\Debug\\avida.exe"
    avida_cwd = "C:\\avida\\build\\bin\\Debug"
    
    try:
        # Signal: パス情報をキューに入れる
        queue_obj.put({"type": "debug", "key": "avida_exe_path", "value": avida_exe})
        queue_obj.put({"type": "debug", "key": "avida_cwd", "value": avida_cwd})
        
        # Start process with explicit cwd and stderr=PIPE
        process = subprocess.Popen(
            [avida_exe],
            cwd=avida_cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Signal: プロセス起動情報をキューに入れる
        queue_obj.put({"type": "debug", "key": "process_pid", "value": str(process.pid)})
        queue_obj.put({"type": "status", "process_started": True})
        
        # スレッド内で stderr を読む関数
        def read_stderr():
            """Read stderr in a separate thread."""
            while True:
                err_line = process.stderr.readline()
                if not err_line:
                    break
                err_line = err_line.strip()
                if err_line:
                    queue_obj.put({"type": "stderr", "line": err_line})
        
        # stderr 読取スレッドを起動
        stderr_thread = threading.Thread(target=read_stderr, daemon=True)
        stderr_thread.start()
        
        # Read stdout line by line
        stdout_count = 0
        queue_count = 0
        
        while True:
            line = process.stdout.readline()
            if not line:
                break
            
            line = line.strip()
            if not line:
                continue
            
            stdout_count += 1
            
            # Send raw line to queue
            queue_obj.put({"type": "raw", "line": line})
            queue_count += 1
            
            # Try to parse and send parsed data
            parsed = parse_avida_line(line)
            if parsed:
                queue_obj.put({
                    "type": "parsed",
                    "ud": parsed["ud"],
                    "gen": parsed["gen"],
                    "fit": parsed["fit"],
                    "orgs": parsed["orgs"]
                })
                queue_count += 1
            else:
                queue_obj.put({"type": "error", "message": f"Failed to parse: {line}"})
                queue_count += 1
        
        # Wait for process to finish
        process.wait()
        exit_code = process.poll()
        
        # Signal: プロセス終了情報をキューに入れる
        queue_obj.put({"type": "debug", "key": "process_exit_code", "value": str(exit_code)})
        queue_obj.put({"type": "debug", "key": "stdout_lines_received", "value": str(stdout_count)})
        queue_obj.put({"type": "debug", "key": "queue_items_sent", "value": str(queue_count)})
        
        # Ensure stderr thread finishes
        stderr_thread.join(timeout=1.0)
        
        queue_obj.put({"type": "status", "process_ended": True})
        
    except Exception as e:
        queue_obj.put({"type": "error", "message": f"Thread error: {str(e)}"})




# ========================================
# キューからデータを処理（メインスレッド）
# ========================================
def process_queue_data():
    """
    Process all available data from queue and update session_state.
    This should be called frequently from the main thread.
    """
    queue_obj = st.session_state.data_queue
    
    while not queue_obj.empty():
        try:
            msg = queue_obj.get_nowait()
            st.session_state.queue_items_received += 1
            
            if msg["type"] == "raw":
                st.session_state.last_raw_line = msg["line"]
                st.session_state.raw_lines.append(msg["line"])
            
            elif msg["type"] == "stderr":
                st.session_state.stderr_lines.append(msg["line"])
            
            elif msg["type"] == "debug":
                key = msg["key"]
                value = msg["value"]
                if key == "process_pid":
                    st.session_state.process_pid = value
                elif key == "process_exit_code":
                    st.session_state.process_exit_code = value
                elif key == "stdout_lines_received":
                    st.session_state.stdout_lines_received = int(value)
                elif key == "avida_exe_path":
                    st.session_state.avida_exe_path = value
                elif key == "avida_cwd":
                    st.session_state.avida_cwd = value
            
            elif msg["type"] == "parsed":
                st.session_state.parse_success += 1
                parsed_data = {
                    "timestamp": datetime.now().isoformat(),
                    "ud": msg["ud"],
                    "gen": msg["gen"],
                    "fit": msg["fit"],
                    "orgs": msg["orgs"]
                }
                st.session_state.parsed_rows.append(parsed_data)
                st.session_state.last_parsed = parsed_data
            
            elif msg["type"] == "error":
                st.session_state.parse_fail += 1
            
            elif msg["type"] == "status":
                if msg.get("process_started"):
                    st.session_state.process_started = True
                if msg.get("process_ended"):
                    st.session_state.running = False
        
        except queue.Empty:
            break




# ========================================
# コントロール関数
# ========================================
def start_simulation():
    """Start the Avida simulation in a background thread."""
    if st.session_state.running:
        st.warning("Simulation already running!")
        return
    
    st.session_state.running = True
    st.session_state.parse_success = 0
    st.session_state.parse_fail = 0
    st.session_state.stdout_lines_received = 0
    st.session_state.queue_items_received = 0
    st.session_state.process_pid = None
    st.session_state.process_exit_code = None
    st.session_state.raw_lines.clear()
    st.session_state.stderr_lines.clear()
    st.session_state.parsed_rows.clear()
    st.session_state.process_started = False
    st.session_state.last_raw_line = ""
    
    # Create and start worker thread
    thread = threading.Thread(
        target=run_avida_simulation,
        args=(st.session_state.data_queue,),
        daemon=True
    )
    st.session_state.worker_thread = thread
    thread.start()


def stop_simulation():
    """Stop the Avida simulation."""
    st.session_state.running = False




# ========================================
# ページ実行
# ========================================

# Initialize session state (main thread)
initialize_session_state()

# Control panel
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("▶ Start", key="start_btn", use_container_width=True):
        start_simulation()

with col2:
    if st.button("⏹ Stop", key="stop_btn", use_container_width=True):
        stop_simulation()

with col3:
    if st.button("🔄 Clear", key="clear_btn", use_container_width=True):
        st.session_state.raw_lines.clear()
        st.session_state.stderr_lines.clear()
        st.session_state.parsed_rows.clear()
        st.session_state.parse_success = 0
        st.session_state.parse_fail = 0
        st.session_state.last_parsed = None
        st.session_state.last_raw_line = ""
        st.session_state.process_pid = None
        st.session_state.process_exit_code = None

# Process queue data (main thread operation)
process_queue_data()

# Debug info panel
with st.expander("🔧 Debug Information", expanded=True):
    st.subheader("Process Information")
    
    debug_col1, debug_col2, debug_col3, debug_col4 = st.columns(4)
    
    with debug_col1:
        st.metric("Process Running", "Yes" if st.session_state.running else "No")
        st.metric("Process Started", "Yes" if st.session_state.process_started else "No")
    
    with debug_col2:
        st.metric("Process PID", st.session_state.process_pid or "N/A")
        st.metric("Exit Code", st.session_state.process_exit_code or "N/A")
    
    with debug_col3:
        st.metric("stdout Lines Received", st.session_state.stdout_lines_received)
        st.metric("Queue Items Received", st.session_state.queue_items_received)
    
    with debug_col4:
        st.metric("Parse Success", st.session_state.parse_success)
        st.metric("Parse Fail", st.session_state.parse_fail)
    
    st.divider()
    
    st.subheader("Paths")
    st.code(f"avida_exe_path: {st.session_state.avida_exe_path}")
    st.code(f"cwd: {st.session_state.avida_cwd}")
    
    st.divider()
    
    st.subheader("Last Raw Line")
    st.code(st.session_state.last_raw_line or "(no data)")
    
    st.subheader("Recent Raw Lines (Last 20)")
    if st.session_state.raw_lines:
        for i, line in enumerate(list(st.session_state.raw_lines)[-20:], 1):
            st.code(f"{i}: {line}", language=None)
    else:
        st.info("No lines yet")
    
    st.divider()
    
    st.subheader("Stderr Lines (Last 20)")
    if st.session_state.stderr_lines:
        for i, line in enumerate(list(st.session_state.stderr_lines)[-20:], 1):
            st.warning(f"{i}: {line}")
    else:
        st.info("No stderr output")
    
    st.divider()
    
    st.subheader("Last Parsed Data")
    if st.session_state.last_parsed:
        st.json(st.session_state.last_parsed)
    else:
        st.info("No parsed data yet")



# Data display section
if st.session_state.parsed_rows:
    st.divider()
    st.subheader("📈 Real-time Graphs")
    
    # Convert deque to list for plotting
    data_list = list(st.session_state.parsed_rows)
    
    # Extract columns for graphing
    indices = list(range(len(data_list)))
    gen_values = [row["gen"] for row in data_list]
    fit_values = [row["fit"] for row in data_list]
    orgs_values = [row["orgs"] for row in data_list]
    
    # Create matplotlib figure with subplots
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    # Gen graph
    axes[0].plot(indices, gen_values, label="Generation", color="blue", linewidth=2)
    axes[0].set_ylabel("Generation")
    axes[0].set_title("Generation Over Time")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    
    # Fit graph
    axes[1].plot(indices, fit_values, label="Fitness", color="green", linewidth=2)
    axes[1].set_ylabel("Fitness")
    axes[1].set_title("Fitness Over Time")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()
    
    # Orgs graph
    axes[2].plot(indices, orgs_values, label="Organisms", color="red", linewidth=2)
    axes[2].set_ylabel("Organisms")
    axes[2].set_xlabel("Data Point")
    axes[2].set_title("Organisms Over Time")
    axes[2].grid(True, alpha=0.3)
    axes[2].legend()
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Data table
    st.subheader("📋 Data Table")
    st.dataframe(
        list(st.session_state.parsed_rows),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("👈 Waiting for data... Click 'Start' to begin simulation.")

# Auto-refresh loop
if st.session_state.running:
    st.rerun()
