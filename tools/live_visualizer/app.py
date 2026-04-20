#!/usr/bin/env python3
"""
Avida Live Visualizer
リアルタイムでAvida シミュレーションの出力をグラフ表示する最小構成
"""

import streamlit as st
import subprocess
import threading
import time
import re
from pathlib import Path
from collections import deque
import matplotlib.pyplot as plt
from typing import Optional, Dict, List
import queue

# ========================================
# ページ設定
# ========================================
st.set_page_config(
    page_title="Avida Live Visualizer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🧬 Avida Live Visualizer")

# ========================================
# 定数設定
# ========================================
AVIDA_EXE = Path(r"C:\avida\build\bin\Debug\avida.exe")
AVIDA_WORK_DIR = Path(r"C:\avida\build\bin\Debug")
MAX_HISTORY = 1000  # グラフに表示する最大データ点数

# ========================================
# Session State 初期化
# ========================================
if "is_running" not in st.session_state:
    st.session_state.is_running = False
    st.session_state.process = None
    st.session_state.thread = None
    st.session_state.data_queue = queue.Queue()  # スレッド間通信用キュー
    st.session_state.data_history = {
        "UD": deque(maxlen=MAX_HISTORY),
        "Gen": deque(maxlen=MAX_HISTORY),
        "Fit": deque(maxlen=MAX_HISTORY),
        "Orgs": deque(maxlen=MAX_HISTORY),
    }
    st.session_state.latest_data = {
        "UD": 0,
        "Gen": 0,
        "Fit": 0.0,
        "Orgs": 0,
    }
    st.session_state.update_count = 0
    st.session_state.error_message = None
    # デバッグ情報
    st.session_state.debug_info = {
        "process_started": False,
        "last_10_lines": deque(maxlen=10),
        "parse_success_count": 0,
        "parse_fail_count": 0,
        "last_parsed_data": None,
        "last_raw_line": None,
    }


# ========================================
# パース関数
# ========================================
def parse_avida_line(line: str) -> Optional[Dict]:
    """
    Avida 出力行をパースする
    
    期待される形式: "UD: 752   Gen: 57.83987   Fit: 0.2486994   Orgs: 3597"
    
    Args:
        line: Avida の出力行
        
    Returns:
        {'UD': int, 'Gen': int, 'Fit': float, 'Orgs': int} または None
    """
    try:
        # 正規表現でパース
        pattern = r'UD:\s*(\d+)\s+Gen:\s*([\d.]+)\s+Fit:\s*([\d.]+)\s+Orgs:\s*(\d+)'
        match = re.search(pattern, line.strip())
        
        if match:
            return {
                "UD": int(match.group(1)),
                "Gen": int(float(match.group(2))),  # Gen は整数に変換
                "Fit": float(match.group(3)),
                "Orgs": int(match.group(4)),
            }
        else:
            return None
    except (ValueError, IndexError, AttributeError):
        return None


# ========================================
# Avida 実行関数（バックグラウンドスレッド）
# ========================================
def run_avida_simulation():
    """
    Avida シミュレーションを実行し、標準出力をリアルタイム読み取り
    ※ Streamlit UI は更新せず、キューにデータを蓄積するだけ
    """
    try:
        # プロセス起動
        process = subprocess.Popen(
            [str(AVIDA_EXE)],
            cwd=str(AVIDA_WORK_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,  # テキストモード
            bufsize=1,  # 行バッファリング
        )
        
        # プロセス起動成功をマーク
        st.session_state.debug_info["process_started"] = True
        
        # 標準出力を行ごとに読み取る
        for line in process.stdout:
            # 停止フラグをチェック
            if not st.session_state.is_running:
                process.terminate()
                break
            
            line = line.strip()
            if not line:
                continue
            
            # デバッグ: 直近10行を保持
            st.session_state.debug_info["last_10_lines"].append(line)
            st.session_state.debug_info["last_raw_line"] = line
            
            # Avida 出力をパース
            data = parse_avida_line(line)
            if data:
                # パース成功
                st.session_state.debug_info["parse_success_count"] += 1
                st.session_state.debug_info["last_parsed_data"] = data
                # データをキューに追加（メインスレッドで処理）
                st.session_state.data_queue.put(data)
            else:
                # パース失敗
                st.session_state.debug_info["parse_fail_count"] += 1
        
        # プロセス終了を待つ
        process.wait()
        
    except Exception as e:
        # エラーメッセージをキューに追加
        st.session_state.data_queue.put({"error": str(e)})
    
    finally:
        st.session_state.is_running = False


# ========================================
# キューからデータを処理（メインスレッド）
# ========================================
def process_data_queue():
    """
    バックグラウンドスレッドから送られたデータを処理
    """
    updated = False
    while not st.session_state.data_queue.empty():
        item = st.session_state.data_queue.get()
        
        if "error" in item:
            st.session_state.error_message = f"エラー: {item['error']}"
            continue
        
        # 正常データの場合
        data = item
        # データを履歴に追加
        st.session_state.data_history["UD"].append(data["UD"])
        st.session_state.data_history["Gen"].append(data["Gen"])
        st.session_state.data_history["Fit"].append(data["Fit"])
        st.session_state.data_history["Orgs"].append(data["Orgs"])
        
        # 最新データを更新
        st.session_state.latest_data = data
        
        # カウント増加
        st.session_state.update_count += 1
        updated = True
    
    return updated


# ========================================
# UI: コントロール
# ========================================
st.subheader("🎮 Control Panel")

col_start, col_stop, col_status = st.columns([1, 1, 2])

with col_start:
    if st.button("▶ Start Simulation", use_container_width=True, key="btn_start"):
        if not st.session_state.is_running:
            # リセット
            st.session_state.data_history = {
                "UD": deque(maxlen=MAX_HISTORY),
                "Gen": deque(maxlen=MAX_HISTORY),
                "Fit": deque(maxlen=MAX_HISTORY),
                "Orgs": deque(maxlen=MAX_HISTORY),
            }
            st.session_state.update_count = 0
            st.session_state.error_message = None
            # デバッグ情報リセット
            st.session_state.debug_info = {
                "process_started": False,
                "last_10_lines": deque(maxlen=10),
                "parse_success_count": 0,
                "parse_fail_count": 0,
                "last_parsed_data": None,
                "last_raw_line": None,
            }
            # キューをクリア
            while not st.session_state.data_queue.empty():
                st.session_state.data_queue.get()
            
            # 実行開始
            st.session_state.is_running = True
            thread = threading.Thread(
                target=run_avida_simulation,
                daemon=True,
            )
            thread.start()
            st.session_state.thread = thread

with col_stop:
    if st.button("⏹ Stop Simulation", use_container_width=True, key="btn_stop"):
        if st.session_state.is_running:
            st.session_state.is_running = False
            if st.session_state.process:
                st.session_state.process.terminate()

with col_status:
    if st.session_state.is_running:
        st.success("🟢 **Running**")
    else:
        st.info("🔴 **Stopped**")

# ========================================
# データ処理（毎回実行）
# ========================================
if st.session_state.is_running or not st.session_state.data_queue.empty():
    if process_data_queue():
        # データが更新されたら再描画
        st.rerun()

# エラーメッセージ表示
if st.session_state.error_message:
    st.error(st.session_state.error_message)

# ========================================
# UI: 統計情報
# ========================================
if st.session_state.update_count > 0 or st.session_state.debug_info["parse_success_count"] > 0:
    st.divider()
    st.subheader("📊 Current Statistics")
    
    metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)
    
    with metric_col1:
        st.metric(
            "Updates",
            st.session_state.update_count,
        )
    
    with metric_col2:
        st.metric(
            "Latest UD",
            st.session_state.latest_data["UD"],
        )
    
    with metric_col3:
        st.metric(
            "Latest Gen",
            st.session_state.latest_data["Gen"],
        )
    
    with metric_col4:
        st.metric(
            "Latest Fit",
            f"{st.session_state.latest_data['Fit']:.4f}",
        )
    
    with metric_col5:
        st.metric(
            "Latest Orgs",
            st.session_state.latest_data["Orgs"],
        )
    
    # ========================================
    # デバッグ情報表示
    # ========================================
    st.divider()
    st.subheader("🐛 Debug Information")
    
    debug_col1, debug_col2, debug_col3 = st.columns(3)
    
    with debug_col1:
        st.metric("Process Started", "Yes" if st.session_state.debug_info["process_started"] else "No")
        st.metric("Parse Success", st.session_state.debug_info["parse_success_count"])
        st.metric("Parse Fail", st.session_state.debug_info["parse_fail_count"])
    
    with debug_col2:
        st.write("**Last 10 Raw Lines:**")
        for i, line in enumerate(st.session_state.debug_info["last_10_lines"]):
            st.code(f"{i+1}: {line}", language=None)
    
    with debug_col3:
        st.write("**Last Parsed Data:**")
        if st.session_state.debug_info["last_parsed_data"]:
            st.json(st.session_state.debug_info["last_parsed_data"])
        else:
            st.write("None")
        
        st.write("**Last Raw Line:**")
        if st.session_state.debug_info["last_raw_line"]:
            st.code(st.session_state.debug_info["last_raw_line"], language=None)
        else:
            st.write("None")
    
    # ========================================
    # グラフ表示
    # ========================================
    st.divider()
    st.subheader("📈 Real-time Graphs")
    
    # x軸（データポイント番号）
    x_data = list(range(len(st.session_state.data_history["Gen"])))
    
    # 図作成（2x2 レイアウト）
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Avida Simulation Data", fontsize=14, fontweight="bold")
    
    # [0,0] Gen (Generation)
    axes[0, 0].plot(
        x_data,
        list(st.session_state.data_history["Gen"]),
        color="blue",
        linewidth=1.5,
        label="Generation",
    )
    axes[0, 0].set_title("Generation (Gen)", fontweight="bold")
    axes[0, 0].set_xlabel("Data Point")
    axes[0, 0].set_ylabel("Gen")
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].legend()
    
    # [0,1] Fit (Fitness)
    axes[0, 1].plot(
        x_data,
        list(st.session_state.data_history["Fit"]),
        color="green",
        linewidth=1.5,
        label="Fitness",
    )
    axes[0, 1].set_title("Fitness (Fit)", fontweight="bold")
    axes[0, 1].set_xlabel("Data Point")
    axes[0, 1].set_ylabel("Fit")
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].legend()
    
    # [1,0] Orgs (Population)
    axes[1, 0].plot(
        x_data,
        list(st.session_state.data_history["Orgs"]),
        color="red",
        linewidth=1.5,
        label="Population",
    )
    axes[1, 0].set_title("Population Size (Orgs)", fontweight="bold")
    axes[1, 0].set_xlabel("Data Point")
    axes[1, 0].set_ylabel("Orgs")
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].legend()
    
    # [1,1] UD (Update)
    axes[1, 1].plot(
        x_data,
        list(st.session_state.data_history["UD"]),
        color="purple",
        linewidth=1.5,
        label="Update",
    )
    axes[1, 1].set_title("Update (UD)", fontweight="bold")
    axes[1, 1].set_xlabel("Data Point")
    axes[1, 1].set_ylabel("UD")
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].legend()
    
    plt.tight_layout()
    st.pyplot(fig)

else:
    st.info(
        "👈 Click **'Start Simulation'** button to begin collecting data and display graphs."
    )
    
    # デバッグ情報表示（データがなくても）
    if st.session_state.debug_info["parse_success_count"] > 0 or st.session_state.debug_info["parse_fail_count"] > 0:
        st.divider()
        st.subheader("🐛 Debug Information (No Graph Data Yet)")
        
        debug_col1, debug_col2 = st.columns(2)
        
        with debug_col1:
            st.metric("Process Started", "Yes" if st.session_state.debug_info["process_started"] else "No")
            st.metric("Parse Success", st.session_state.debug_info["parse_success_count"])
            st.metric("Parse Fail", st.session_state.debug_info["parse_fail_count"])
        
        with debug_col2:
            st.write("**Last Raw Line:**")
            if st.session_state.debug_info["last_raw_line"]:
                st.code(st.session_state.debug_info["last_raw_line"], language=None)
            else:
                st.write("None")

# ========================================
# サイドバー：情報
# ========================================
st.sidebar.subheader("ℹ️ Information")
st.sidebar.write(f"**Avida Executable:** {AVIDA_EXE}")
st.sidebar.write(f"**Working Directory:** {AVIDA_WORK_DIR}")
st.sidebar.write(f"**Max History Points:** {MAX_HISTORY}")

st.sidebar.divider()
st.sidebar.write("""
### How to Use
1. Click **Start Simulation** to begin
2. Watch real-time data displayed in the graphs
3. Metrics update as new data arrives
4. Click **Stop Simulation** to end
""")
