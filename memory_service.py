try:
    import pysqlite3
    import sys
    # 這是為了解決 Streamlit Cloud 或舊版 Linux 環境 SQLite 版本過低的問題
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

import chromadb
from chromadb.config import Settings
from datetime import datetime
import os
import uuid

class MemoryService:
    def __init__(self):
        # 建議將 DB 路徑設為絕對路徑，避免 WSL 執行路徑混淆
        self.db_path = os.path.join(os.getcwd(), "chroma_db")
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)
            
        try:
            # 2026 推薦配置：增加緩存與持久化可靠性
            self.client = chromadb.PersistentClient(
                path=self.db_path,
                settings=Settings(
                    allow_reset=True,
                    anonymized_telemetry=False,
                    is_persistent=True # 確保寫入磁碟
                )
            )
            print(f"✅ ChromaDB 已成功掛載至: {self.db_path}")
        except Exception as e:
            print(f"⚠️ 持久化存儲失敗，切換至記憶體模式 (重啟後記憶會消失): {e}")
            self.client = chromadb.EphemeralClient()
        
        # 取得或建立集合
        # 註：此處預設會加載本地 Embedding 模型，若 WSL 依然崩潰，建議改用 OpenAI Embedding API
        self.collection = self.client.get_or_create_collection(
            name="long_term_memory",
            metadata={"hnsw:space": "cosine"} # 使用餘弦相似度，適合對話匹配
        )

    def save_to_memory(self, session_id, user_msg, assistant_msg):
        """將對話存入向量資料庫"""
        if not user_msg.strip(): return
        
        combined_text = f"用戶提問: {user_msg}\n助手回答: {assistant_msg}"
        timestamp = datetime.now().isoformat()
        
        try:
            self.collection.add(
                documents=[combined_text],
                ids=[str(uuid.uuid4())], # 使用 UUID 避免 ID 衝突
                metadatas=[{
                    "session_id": session_id, 
                    "timestamp": timestamp,
                    "type": "conversation"
                }]
            )
        except Exception as e:
            print(f"❌ 儲存記憶失敗: {e}")

    def search_memory(self, query, n_results=3):
        """檢索相關記憶"""
        if not query.strip(): return ""
        
        try:
            # 增加一個相似度閾值過濾（可選）
            results = self.collection.query(
                query_texts=[query], 
                n_results=n_results
            )
            
            if results and results['documents'] and len(results['documents'][0]) > 0:
                # 組合檢索到的記憶，並加上分隔線
                memories = results['documents'][0]
                formatted_memory = "\n---\n".join(memories)
                return formatted_memory
            return ""
        except Exception as e:
            print(f"❌ 檢索記憶出錯: {e}")
            return ""

    def clear_session_memory(self, session_id):
        """刪除特定會話的記憶（選配功能）"""
        try:
            self.collection.delete(where={"session_id": session_id})
        except Exception as e:
            print(f"❌ 刪除記憶失敗: {e}")