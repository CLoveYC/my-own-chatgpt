try:
    import pysqlite3
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

import streamlit as st
import asyncio
from datetime import datetime
from llm_service import LLMService
from memory_service import MemoryService
from ui_components import render_sidebar, save_session_data, load_session_data

# 頁面配置
st.set_page_config(page_title="Ultimate AI Agent", layout="wide", page_icon="🤖")

# --- 1. 服務實例化 (使用緩存優化) ---
@st.cache_resource
def get_services():
    # 初始化 LLM (啟用 Async) 與 Memory
    return LLMService(), MemoryService()

llm, memory = get_services()

# --- 2. 初始化 Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.current_title = "新對話"
    st.session_state.system_instruction = "你是一個強大的 AI 助手，擁有多模態、聯網搜尋與長期記憶能力。"

# --- 3. 渲染側邊欄 ---
# 傳入當前會話資訊，並獲取音頻上傳與 UI 設定
audio_file = render_sidebar()

st.title("🤖 智聯全功能助手")
st.caption(f"當前會話 ID: {st.session_state.current_session_id} | 模式: {'智慧路由' if st.session_state.get('auto_route') else '標準'}")

# --- 4. 顯示對話歷史紀錄 ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. 輸入源處理 (音頻 or 文本) ---
prompt = None

# A. 處理音頻輸入
if audio_file is not None:
    # 使用檔案名稱作為緩存 Key，避免重複轉錄同一檔案
    if st.session_state.get("last_processed_audio") != audio_file.name:
        with st.status("🎙️ 正在進行雲端語音轉錄...", expanded=True) as status:
            # 呼叫 Async 轉錄方法
            transcribed_text = llm.transcribe_audio(audio_file)
            if "失敗" not in transcribed_text:
                status.update(label="✓ 轉錄完成", state="complete")
                prompt = transcribed_text
                st.session_state.last_processed_audio = audio_file.name
            else:
                status.update(label="❌ 轉錄失敗", state="error")
                st.error(transcribed_text)
    else:
        # 如果已經轉錄過且沒有新的文本輸入，則保持靜默 (避免循環)
        pass

# B. 處理文本輸入 (如果音頻沒有產生 prompt)
chat_input = st.chat_input("詢問任何事，或點擊左側上傳音頻...")
if chat_input:
    prompt = chat_input

# --- 6. 核心處理邏輯 (當有 prompt 時觸發) ---
if prompt:
    # 步驟 1: 顯示並記錄使用者訊息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 步驟 2: 檢索長期記憶 (RAG)
    context = ""
    if st.session_state.get("use_memory"):
        with st.status("正在檢索相關記憶...", expanded=False):
            context = memory.search_memory(prompt)
            if context:
                st.write("已找到相關歷史背景")

    # 步驟 3: 生成助理回應
    with st.chat_message("assistant"):
        # 決定使用的模型 (路由邏輯已封裝在 LLMService)
        with st.spinner("AI 思考中..."):
            # 準備訊息 (注入背景)
            api_messages = st.session_state.messages.copy()
            if context:
                api_messages[-1] = {
                    "role": "user", 
                    "content": f"【相關歷史背景】:\n{context}\n\n【目前的提問】: {prompt}"
                }

            # 呼叫非同步 LLM 服務 (含 Tool Use 邏輯)
            try:
                response = llm.get_chat_response(
                    messages=api_messages,
                    system_instruction=st.session_state.system_instruction
                )
                st.markdown(response)
            except Exception as e:
                response = f"❌ API 執行錯誤: {str(e)}"
                st.error(response)

    # 步驟 4: 更新與存檔
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # 存入長期記憶
    if st.session_state.get("use_memory"):
        memory.save_to_memory(st.session_state.current_session_id, prompt, response)

    # 處理標題生成 (第一輪對話)
    is_new_session = len(st.session_state.messages) <= 2
    if is_new_session:
        new_title = llm.generate_title(prompt)
        st.session_state.current_title = new_title
    
    # 儲存對話到檔案
    save_session_data(
        st.session_state.current_session_id,
        st.session_state.current_title,
        st.session_state.system_instruction,
        st.session_state.messages
    )
    
    # 若是新對話，強制重新渲染以更新側邊欄標題列表
    if is_new_session:
        st.rerun()