# My Own ChatGPT - Advanced AI Assistant

這是一個基於 **Streamlit** 開發的高性能 ChatGPT 網頁應用程式，專為網工所 HW1 作業設計。本專案透過串接 **Groq API** 提供極速的 LLM 推論體驗，並具備多對話管理、智慧標題生成、以及全方位的模型參數控制功能。

## 🚀 核心亮點 (Core Features)

- **智慧標題 (Smart AI Title)**：系統會自動調用 Llama 3.1 8B 模型，根據使用者的首條訊息語義總結出精簡標題，而非生硬截斷。
- **多對話管理 (Multi-Session CRUD)**：支援建立多組獨立對話，資料以 JSON 格式持久化存儲於本地，支援歷史紀錄切換與刪除。
- **進階參數控制 (Advanced Playground)**：
  - **Temperature**: 控制隨機性。
  - **Top-P**: 控制詞彙多樣性。
  - **Max Tokens**: 限制回答長度。
  - **Presence Penalty**: 鼓勵或減少話題重複。
- **系統指令 (System Instruction)**：支援動態設定 AI 的人設（Persona），並能隨對話紀錄獨立儲存。
- **現代化工具鏈 (Modern Tech Stack)**：使用 `uv` 進行套件管理，確保環境乾淨且安裝極速。
- **串流輸出 (Streaming Response)**：完美模擬 ChatGPT 的逐字輸出效果。

---

## 🛠️ 技術棧 (Tech Stack)

- **Frontend**: Streamlit
- **Backend**: Python 3.11+
- **LLM API**: Groq (Llama-3.3-70B, Mixtral, Gemma 2)
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Data Storage**: Local JSON Files

---

## 📦 安裝與環境設定 (Installation)

### 1. 安裝 uv
如果你尚未安裝 `uv`，請執行：
```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 複製專案與安裝依賴
```bash
git clone https://github.com/CLoveYC/my-own-chatgpt
cd my-own-chatgpt

# 使用 uv 自動同步並建立虛擬環境
uv sync
```

### 3. 設定 API Key
在專案根目錄建立 `.env` 檔案，並填入你的 Groq API Key：
```env
GROQ_API_KEY=gsk_your_api_key_here
```
*(註：本專案已將 `.env` 加入 `.gitignore` 以保護私鑰安全)*

---

## 🏃 啟動程式

使用 `uv` 一鍵啟動 Web 服務：
```bash
uv run streamlit run app.py
```
啟動後，瀏覽器會自動開啟 `http://localhost:8501`。

---

## 📂 專案結構 (Project Structure)

```text
├── app.py              # 程式主入口，負責頁面流程與狀態控制
├── llm_service.py      # LLM 邏輯層，封裝 API 呼叫與標題生成
├── ui_components.py    # UI 組件層，負責側邊欄渲染與檔案讀寫
├── sessions/           # 儲存對話紀錄的 JSON 資料夾 (自動建立)
├── .env                # 環境變數 (私密金鑰)
├── .gitignore          # 排除 sessions/ 與 .env 上傳
└── pyproject.toml      # uv 專案定義文件
```

`[Demo Video Link](https://youtu.be/JxjCjyTRfsk)`