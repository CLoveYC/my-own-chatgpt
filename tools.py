# tools.py
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup

def web_search(query: str):
    """當需要獲取即時新聞、天氣、或最近發生的事件時，使用此工具搜尋網際網路。"""
    try:
        with DDGS() as ddgs:
            # 獲取前 5 筆結果
            results = [r for r in ddgs.text(query, max_results=5)]
            if not results:
                return "搜尋不到相關結果。"
            
            # 格式化輸出以便 LLM 閱讀
            formatted_res = ""
            for i, r in enumerate(results):
                formatted_res += f"[{i+1}] 標題: {r['title']}\n連結: {r['href']}\n摘要: {r['body']}\n\n"
            return formatted_res
    except Exception as e:
        return f"搜尋出錯: {e}"

def get_page_content(url: str):
    """當搜尋結果中的摘要不夠詳細，需要深入閱讀某個網址的具體內容時使用。"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 移除腳本與樣式
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator=' ', strip=True)
        return text[:2500] # 限制字數避免 Token 爆炸
    except Exception as e:
        return f"無法讀取網頁內容: {e}"

# OpenAI 格式的工具定義清單
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "搜尋網際網路以獲取最新資訊",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜尋關鍵字"}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_page_content",
            "description": "讀取指定網址的詳細文字內容",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "目標網址"}
                },
                "required": ["url"],
            },
        },
    }
]

# 工具執行映射
AVAILABLE_TOOLS = {
    "web_search": web_search,
    "get_page_content": get_page_content,
}