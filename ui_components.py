import streamlit as st
import os
import json
from datetime import datetime

SESSIONS_DIR = "sessions"
if not os.path.exists(SESSIONS_DIR):
    os.makedirs(SESSIONS_DIR)

def load_session_data(session_id):
    path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return {"title": "舊對話", "system_instruction": "你是一個專業助手。", "messages": data}
            return data
    return {"title": "新對話", "system_instruction": "你是一個專業助手。", "messages": []}

def save_session_data(session_id, title, system_instruction, messages):
    if session_id:
        path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
        data = {"title": title, "system_instruction": system_instruction, "messages": messages}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def display_chat_messages(messages):
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

def render_sidebar():
    with st.sidebar:
        st.title("💬 對話管理")
        if st.button("➕ 啟動新對話", use_container_width=True):
            st.session_state.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.session_state.messages = []
            st.session_state.current_title = "新對話"
            st.session_state.system_instruction = "你是一個專業助手。" # 重置預設指令
            st.rerun()

        st.divider()
        files = sorted([f for f in os.listdir(SESSIONS_DIR) if f.endswith(".json")], reverse=True)
        for f in files:
            session_id = f.replace(".json", "")
            data = load_session_data(session_id)
            display_title = data.get("title", "新對話")
            is_current = (st.session_state.get("current_session_id") == session_id)
            
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                icon = "⭐" if is_current else "📄"
                if st.button(f"{icon} {display_title}", key=f"s_{session_id}", use_container_width=True):
                    st.session_state.current_session_id = session_id
                    st.session_state.messages = data.get("messages", [])
                    st.session_state.current_title = data.get("title", "新對話")
                    st.session_state.system_instruction = data.get("system_instruction", "你是一個專業助手。")
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"d_{session_id}"):
                    os.remove(os.path.join(SESSIONS_DIR, f))
                    if st.session_state.current_session_id == session_id:
                        st.session_state.current_session_id = None
                    st.rerun()

        st.divider()
        st.title("⚙️ 模型設定")
        
        # 🔥 【新增】System Instruction 輸入框
        system_instruction = st.text_area(
            "系統指令 (System Instruction)", 
            value=st.session_state.get("system_instruction", "你是一個專業助手。"),
            help="在這裡定義 AI 的人設或說話風格",
            height=100
        )
        # 即時更新 session_state 確保存檔時抓到最新指令
        st.session_state.system_instruction = system_instruction

        model = st.selectbox("選擇模型", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "qwen/qwen3-32b", "openai/gpt-oss-120b"])
        
        with st.expander("🛠️ 進階參數"):
            temp = st.slider("溫度 (Temp)", 0.0, 2.0, 0.7, 0.1)
            top_p = st.slider("核取樣 (Top-P)", 0.0, 1.0, 1.0, 0.1)
            max_t = st.number_input("最大長度", 128, 8192, 2048)
            p_pen = st.slider("存在懲罰", -2.0, 2.0, 0.0, 0.1)
            
        return model, system_instruction, temp, top_p, max_t, p_pen