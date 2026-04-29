# 🤖 Ultimate AI Agent (2026 Edition)

這是一個基於 **Groq LPU** 加速技術開發的高效能 AI 代理人系統。整合了長期記憶 (RAG)、語音多模態 (STT)、智慧模型路由以及聯網工具 (Web Search)，旨在提供亞秒級的智慧交互體驗。

## 🚀 核心功能 (Key Features)

### 1. 🧠 長期記憶 (Long-term Memory / RAG)
透過 **ChromaDB** 向量資料庫實現。系統會自動對每輪對話進行語意索引，並在後續對話中主動檢索相關背景，解決 LLM 遺忘歷史資訊的問題。
- **向量嵌入**: 使用 ChromaDB 內建模型進行語意匹配
- **持久化存儲**: 支援本地文件存儲，重啟後記憶依然保留
- **自動索引**: 每次對話自動保存到記憶庫

### 2. 🎙️ 語音多模態 (Multimodal STT)
整合 **Whisper-large-v3-turbo** 雲端引擎。支援多種音訊格式上傳，達成極速語音轉文字，實現流暢的語音交互。
- 支援 WAV、MP3、M4A 等多種音訊格式
- 雲端處理，無需本地模型資源
- 自動緩存，避免重複轉錄

### 3. 🛣️ 智慧路由 (Auto-Routing)
系統會根據使用者提問的複雜度自動切換模型：
- **Llama-3.1-8b-instant**: 用於日常問候與簡單任務（追求極速回應）
- **Llama-3.3-70b-versatile**: 用於深度分析、程式開發與聯網搜尋（追求邏輯推理）

### 4. 🌐 聯網搜尋工具 (Web Search & Tool Use)
整合 **DuckDuckGo Search** 與網頁抓取工具。AI 能主動判斷是否需要搜尋即時資訊。
- **Web 搜尋**: 自動搜尋最新新聞、股價、天氣等即時資訊
- **網頁解析**: 深入抓取搜尋結果頁面內容，提供更詳細資訊
- **工具調用**: 基於 OpenAI 函數調用格式，完全相容 Groq API

---

## 🛠️ 技術架構 (Tech Stack)

| 元件 | 技術 | 用途 |
|------|------|------|
| **LLM 引擎** | Groq (Llama 3.3-70B / 3.1-8B) | 對話生成與推理 |
| **向量資料庫** | ChromaDB 1.5.8+ | 長期記憶與 RAG 檢索 |
| **語音轉文字** | Groq Whisper API | 音訊輸入處理 |
| **網路搜尋** | DuckDuckGo Search | 即時資訊獲取 |
| **網頁解析** | BeautifulSoup 4 | 網頁內容提取 |
| **前端框架** | Streamlit 1.55+ | Web UI 介面 |
| **HTTP 客戶端** | OpenAI Python SDK | API 呼叫 |

---

## 📁 項目結構

```
my-own-chatgpt/
├── app.py                      # 主應用程式 (Streamlit 入口)
├── llm_service.py              # LLM 服務類 (Groq API 互動、模型路由、工具調用)
├── memory_service.py           # 記憶服務類 (ChromaDB 向量存儲)
├── tools.py                    # 工具定義 (Web 搜尋、網頁內容提取)
├── ui_components.py            # UI 組件 (側邊欄、對話渲染、會話管理)
├── pyproject.toml              # 專案配置與依賴管理
├── chroma_db/                  # ChromaDB 本地資料庫目錄
│   └── chroma.sqlite3          # 向量資料庫檔案
├── sessions/                   # 對話會話備份
│   └── *.json                  # 每個會話的完整對話紀錄
└── README.md                   # 本檔案
```

---

## 📦 安裝與設置指南

### 系統需求
- **Python**: 3.11 或以上版本
- **作業系統**: Linux、macOS 或 WSL 環境（建議不使用原生 Windows CMD）
- **磁碟空間**: 至少 500MB（ChromaDB 與模型快取）

### 1️⃣ 複製專案
```bash
git clone https://github.com/your-username/my-own-chatgpt.git
cd my-own-chatgpt
```

### 2️⃣ 建立虛擬環境 (推薦)
```bash
# Linux / macOS / WSL
python -m venv .venv
source .venv/bin/activate

# Windows CMD (不推薦，但如果要用)
python -m venv .venv
.venv\Scripts\activate
```

### 3️⃣ 安裝依賴
```bash
pip install -r requirements.txt
```

或透過 pyproject.toml：
```bash
pip install -e .
```

單獨安裝的方式：
```bash
pip install \
  streamlit>=1.55.0 \
  openai>=2.29.0 \
  chromadb>=1.5.8 \
  duckduckgo-search>=8.1.1 \
  beautifulsoup4>=4.14.3 \
  python-dotenv>=1.2.2 \
  pysqlite3-binary>=0.5.4.post2 \
  requests>=2.32.5 \
  google-genai>=1.73.1 \
  google-generativeai>=0.8.6
```

### 4️⃣ 設置環境變數
在專案根目錄建立 `.env` 檔案，填入您的 API 金鑰：

```env
# 必需：Groq API 金鑰 (從 https://console.groq.com 取得)
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx

# 可選：其他 LLM API (如需額外模型)
OPENAI_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxx
GOOGLE_API_KEY=xxxxxxxxxxxxxxxxxxxxx
```

**⚠️ 重要**: 
- 絕不要將 `.env` 提交到 Git（已在 `.gitignore` 中）
- 免費 Groq API 有配額限制，請勿濫用

### 5️⃣ 首次執行
```bash
streamlit run app.py
```

應用將在 `http://localhost:8501` 啟動。

---

## 🎯 使用指南

### 基本互動
1. **文本輸入**: 在下方輸入框輸入問題
2. **語音輸入**: 左側邊欄點擊「上傳音訊」，選擇音檔
3. **自動路由**: 系統自動偵測複雜度，選擇合適模型
4. **記憶檢索**: 若啟用「使用長期記憶」，系統會自動從歷史中查找相關背景

### 設定說明

| 設定項 | 說明 | 預設值 |
|--------|------|--------|
| 使用長期記憶 | 啟用 RAG，檢索歷史對話背景 | ✅ 啟用 |
| 智慧路由 | 自動選擇模型（簡單快速/複雜深度） | ✅ 啟用 |
| 系統提示詞 | AI 助手的行為角色定義 | 強大的 AI 助手 |

### 觸發智慧搜尋的關鍵詞
模型會自動判斷以下情況需要搜尋：
- `"搜尋"` 或 `"查一下"`
- `"分析"` 或 `"比較"`
- `"程式"` 或 `"代碼"`
- `"比特幣"` 或其他金融主題

---

## 🔧 架構詳解

### 會話流程圖
```
使用者輸入 (文字/語音)
    ↓
[llm_service.transcribe_audio] (如果是語音)
    ↓
[memory_service.search_memory] (檢索相關背景)
    ↓
[llm_service.route_model] (決定使用哪個模型)
    ↓
[Groq API 呼叫 + 工具調用]
    ↓
[tools.web_search / get_page_content] (如果需要)
    ↓
[memory_service.save_to_memory] (保存對話到記憶)
    ↓
UI 渲染回應 + 保存會話
```

### 核心類別

#### `LLMService`
- `route_model(prompt)`: 根據提問複雜度選擇模型
- `get_chat_response(messages, system_instruction)`: 調用 Groq API，處理工具呼叫
- `transcribe_audio(audio_file)`: 語音轉文字
- `generate_title(text)`: 根據對話生成會話標題

#### `MemoryService`
- `save_to_memory(session_id, user_msg, assistant_msg)`: 將對話存入 ChromaDB
- `search_memory(query)`: 檢索相關歷史對話背景
- `clear_memory()`: 清空記憶庫

#### `Tools`
- `web_search(query)`: DuckDuckGo 搜尋 (返回前 5 筆結果)
- `get_page_content(url)`: 抓取網頁內容 (限制 2500 字元)

---

## 🐛 常見問題與解決方案

### 問題 1: ChromaDB SQLite 版本錯誤
**症狀**: `ImportError: cannot import name 'Row'` 或 `sqlite3.DatabaseError`

**解決方案**:
```python
# app.py 已包含修復，若仍有問題，確保 pysqlite3-binary 已安裝
pip install --upgrade pysqlite3-binary
```

### 問題 2: Groq API 配額用盡
**症狀**: `RateLimitError: 429 Too Many Requests`

**解決方案**:
- 檢查 API 金鑰是否正確
- 等待配額重置（通常為 24 小時）
- 使用付費 Groq 帳戶獲得更高配額

### 問題 3: ChromaDB 無法持久化
**症狀**: 重啟後記憶消失，出現「切換至記憶體模式」警告

**解決方案**:
```bash
# 確保有寫入權限
chmod -R 755 chroma_db/

# 或重新初始化資料庫
rm -rf chroma_db/
# 重啟應用會自動重建
```

### 問題 4: Streamlit 無法在 WSL 中啟動
**症狀**: `ModuleNotFoundError` 或無法連接到 localhost:8501

**解決方案**:
```bash
# 確保在 WSL 終端執行（不要在 Windows CMD）
source .venv/bin/activate
streamlit run app.py --server.address localhost
```

---

## 🚀 進階功能

### 自訂系統提示詞
在側邊欄修改「系統提示詞」欄位，例如：
```
你是一位專業的軟體工程師，精通 Python、JavaScript 與 DevOps。
回答時需附帶程式範例與最佳實踐建議。
```

### 批量導入記憶
如需從外部檔案導入對話歷史：
```python
from memory_service import MemoryService

memory = MemoryService()
# 手動呼叫 save_to_memory 批量插入
memory.save_to_memory("session_id", "用戶提問", "助手回答")
```

### 使用其他 LLM 提供商
修改 `llm_service.py` 中的 `self.client` 初始化，例如改用 OpenAI：
```python
self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

---

## 📊 效能指標

基於 Groq 官方基準測試（2026 年 4 月）：

| 指標 | Llama 3.1-8B | Llama 3.3-70B |
|------|------------|-------------|
| 首字元延遲 (TTFT) | <100ms | <200ms |
| 輸出吞吐量 | 80-120 tokens/sec | 100-150 tokens/sec |
| 推薦用途 | 簡單問答、即時聊天 | 程式開發、邏輯分析 |

---

## 🤝 開發與貢獻

### 開發環境設置
```bash
# 安裝開發依賴
pip install pytest pytest-asyncio black flake8

# 執行測試
pytest tests/
```

### 程式風格
- 遵循 PEP 8 規範
- 使用 `black` 進行自動格式化
- 註解使用繁體中文，便於理解

### 提交流程
1. Fork 本倉庫
2. 建立特性分支 (`git checkout -b feature/your-feature`)
3. 提交更改 (`git commit -am 'Add new feature'`)
4. 推送到分支 (`git push origin feature/your-feature`)
5. 開啟 Pull Request

---

## 📜 許可證

本專案採用 **MIT 許可證**。詳見 [LICENSE](LICENSE) 檔案。

---

## 📞 聯繫與支援

如有問題或建議，歡迎：
- 提交 [GitHub Issues](https://github.com/your-username/my-own-chatgpt/issues)
- 發起 [Discussions](https://github.com/your-username/my-own-chatgpt/discussions)
- 發送電子郵件至 your-email@example.com

---

## 🙏 致謝

感謝以下開源專案與服務的支援：

- [Groq](https://groq.com) - LLM 推理加速
- [ChromaDB](https://www.trychroma.com) - 向量資料庫
- [Streamlit](https://streamlit.io) - Web 應用框架
- [DuckDuckGo](https://duckduckgo.com) - 隱私搜尋引擎

---

**最後更新**: 2026 年 4 月 29 日  
**版本**: 0.1.0