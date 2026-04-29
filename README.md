# 🤖 Ultimate AI Agent (2026 Edition)

這是一個基於 **Groq LPU** 加速技術開發的高效能 AI 代理人系統。整合了長期記憶 (RAG)、語音多模態 (STT)、智慧模型路由以及聯網工具 (MCP)，旨在提供亞秒級的智慧交互體驗。

## 🚀 核心功能 (Key Features)

### 1. 🧠 長期記憶 (Long-term Memory)
透過 **ChromaDB** 向量資料庫實現。系統會自動對每輪對話進行語意索引，並在後續對話中主動檢索相關背景，解決 LLM 遺忘歷史資訊的問題。

### 2. 🎙️ 語音多模態 (Multimodal STT)
整合 **Whisper-large-v3-turbo** 雲端引擎。支援多種音訊格式上傳，達成極速語音轉文字，實現流暢的語音交互。

### 3. 🛣️ 智慧路由 (Auto-Routing)
系統會根據任務複雜度自動切換模型：
- **Llama-3.1-8b-instant**: 用於日常問候與簡單任務（追求極速）。
- **Llama-3.3-70b-versatile**: 用於深度分析、程式開發與聯網搜尋（追求邏輯）。

### 4. 🌐 聯網搜尋與 MCP 工具 (Tool Use)
整合 **DuckDuckGo Search** 與網頁抓取工具。AI 能主動判斷是否需要搜尋即時事實（如幣價、新聞），並透過工具獲取最新資訊。

---

## 🛠️ 技術架構 (Tech Stack)

- **LLM Engine**: Groq (Llama 3.3-70B / 3.1-8B)
- **Vector DB**: ChromaDB (with `pysqlite3-binary` fix)
- **Speech-to-Text**: Groq Cloud Whisper API
- **Web Search**: DuckDuckGo Search (DDGS)
- **Backend/UI**: Streamlit

---

## 📦 安裝指南 (Installation)

### 1. 複製專案
```bash
git clone https://github.com/your-username/my-own-chatgpt.git
cd my-own-chatgpt
```

### 2. 建立虛擬環境 (Recommended)
```bash
python -m venv .venv
source .venv/bin/activate  # WSL/Linux
```

### 3. 安裝依賴
```bash
pip install streamlit openai chromadb duckduckgo-search beautifulsoup4 python-dotenv pysqlite3-binary requests
```

### 4. 環境變數設定
在專案根目錄建立 `.env` 檔案：
```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## 🖥️ 使用說明 (Usage)

啟動應用程式：
```bash
streamlit run app.py
```

### 💡 Demo 建議指令
- **搜尋功能**: 「搜尋目前的比特幣價格並總結一則最新新聞。」
- **記憶功能**: 「我剛才說過我住在哪裡？」
- **語音功能**: 直接上傳一個音訊檔，詢問其中的內容。

---

## 📂 專案結構 (Project Structure)

- `app.py`: 主程式與 Streamlit UI 邏輯。
- `llm_service.py`: 處理 LLM 請求、智慧路由與工具呼叫核心。
- `memory_service.py`: 負責向量數據儲存與 RAG 檢索。
- `tools.py`: 定義 Web 搜尋與網頁抓取等外部工具。
- `ui_components.py`: 側邊欄渲染與對話 Session 管理。

---

## 📜 授權協議 (License)
本專案採用 [MIT License](LICENSE) 授權。

---
**開發者**: CLoveYC
**更新日期**: 2026-04-29