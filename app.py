import streamlit as st
from datetime import datetime
from llm_service import LLMService
from ui_components import render_sidebar, display_chat_messages, save_session_data, load_session_data

st.set_page_config(page_title="My AI ChatGPT", layout="centered")

# 初始化
if "current_session_id" not in st.session_state or st.session_state.current_session_id is None:
    st.session_state.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.messages = []
    st.session_state.current_title = "新對話"
    st.session_state.system_instruction = "你是一個專業助手。"

# 側邊欄 (多接收一個 system_instruction)
model, sys_inst, temp, top_p, max_t, p_pen = render_sidebar()

st.title("🤖 My Smart ChatGPT")

# 顯示訊息
display_chat_messages(st.session_state.messages)

# 輸入
if prompt := st.chat_input("跟我聊聊吧..."):
    is_first_msg = (len(st.session_state.messages) == 0)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        llm = LLMService()
        
        # 🔥 傳入系統指令
        stream = llm.get_chat_response(model, st.session_state.messages, sys_inst, temp, top_p, max_t, p_pen)
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                full_response += content
                placeholder.markdown(full_response + "▌")
        placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # 生成智慧標題
    if is_first_msg:
        with st.spinner("思考標題中..."):
            st.session_state.current_title = llm.generate_title(prompt)
    
    # 🔥 存檔 (包含系統指令)
    save_session_data(
        st.session_state.current_session_id, 
        st.session_state.current_title, 
        sys_inst, 
        st.session_state.messages
    )

    if is_first_msg:
        st.rerun()