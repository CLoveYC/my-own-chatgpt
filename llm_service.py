import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.groq.com/openai/v1")

    def get_chat_response(self, model, messages, system_instruction, temperature, top_p, max_tokens, presence_penalty):
        # 🔥 將使用者設定的 System Instruction 放在最前面
        full_messages = [{"role": "system", "content": system_instruction}] + messages
        
        return self.client.chat.completions.create(
            model=model,
            messages=full_messages,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            presence_penalty=presence_penalty,
            stream=True
        )

    def generate_title(self, user_input):
        try:
            res = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "總結句子成5字內繁體中文標題，無標點，只回文字。"},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=20,
                temperature=0.3
            )
            title = res.choices[0].message.content.strip().replace("。", "").replace('"', "")
            return title[:6]
        except:
            return user_input[:6]