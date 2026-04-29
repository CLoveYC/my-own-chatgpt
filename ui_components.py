import streamlit as st
import os
import json
from datetime import datetime

# 設定存檔目錄
SESSIONS_DIR = "sessions"
if not os.path.exists(SESSIONS_DIR): 
    os.makedirs(SESSIONS_DIR)

def load_session_data(session_id):
    """從 JSON 載入會話紀錄"""
    path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None

def save_session_data(session_id, title, system_instruction, messages):
    """儲存目前會話到 JSON"""
    if session_id and messages:
        path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
        data = {
            "title": title, 
            "system_instruction": system_instruction, 
            "messages": messages,
            "last_updated": datetime.now().isoformat()
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def delete_session(session_id):
    """刪除特定的會話檔案"""
    path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
    if os.path.exists(path):
        os.remove(path)
        return True
    return False

def render_sidebar():
    """渲染側邊欄並返回上傳的音頻文件"""
    with st.sidebar:
        st.title("🧠 Agent 控制中心")
        
        # 1. 新對話按鈕
        if st.button("➕ 開啟新對話", use_container_width=True, type="primary"):
            st.session_state.messages = []
            st.session_state.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.session_state.current_title = "新對話"
            st.rerun()

        st.divider()

        # 2. 核心功能切換 (使用 Expander 節省空間)
        with st.expander("🛠️ 核心功能設定", expanded=True):
            st.session_state.use_memory = st.toggle("開啟長期記憶 (RAG)", value=st.session_state.get("use_memory", True))
            st.session_state.auto_route = st.toggle("智慧路由模型 (LLama 3.3)", value=st.session_state.get("auto_route", True))
            
            # 允許動態修改 System Prompt
            new_instruction = st.text_area(
                "系統指令 (System Prompt)", 
                value=st.session_state.get("system_instruction", "你是一個強大的 AI 助手。"),
                height=100
            )
            st.session_state.system_instruction = new_instruction

        st.divider()

        # 3. 語音輸入區
        st.subheader("🎙️ 語音轉錄")
        audio_file = st.file_uploader("上傳音訊 (Groq Cloud 加速)", type=["mp3", "wav", "m4a", "flac", "ogg"])
        
        st.divider()

        # 4. 歷史紀錄管理
        st.subheader("📜 歷史紀錄")
        
        # 獲取所有檔案並按時間排序
        files = sorted(
            [f for f in os.listdir(SESSIONS_DIR) if f.endswith(".json")], 
            key=lambda x: os.path.getmtime(os.path.join(SESSIONS_DIR, x)), 
            reverse=True
        )

        for f in files:
            sid = f.replace(".json", "")
            # 這裡不讀取完整內容，只讀取標題以優化效能
            data = load_session_data(sid)
            if not data: continue
            
            title = data.get("title", "無標題")
            
            # 使用 Columns 製作「選擇」與「刪除」按鈕排版
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                # 標示當前正在使用的會話
                btn_type = "secondary"
                if st.session_state.get("current_session_id") == sid:
                    title = f"▶ {title}"
                
                if st.button(f"{title[:12]}", key=f"load_{sid}", use_container_width=True):
                    st.session_state.current_session_id = sid
                    st.session_state.messages = data['messages']
                    st.session_state.current_title = data['title']
                    st.session_state.system_instruction = data.get('system_instruction', st.session_state.system_instruction)
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"del_{sid}", help="刪除此對話"):
                    if delete_session(sid):
                        if st.session_state.get("current_session_id") == sid:
                            st.session_state.messages = []
                            st.session_state.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
                        st.rerun()

        # 頁腳版本資訊
        st.divider()
        st.caption("Ultimate Agent v2.0 (2026) | Powered by Groq & Llama 3")

        return audio_file