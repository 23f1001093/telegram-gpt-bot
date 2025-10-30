import httpx
from src.config import OPENAI_API_KEY

async def get_gpt_reply(messages):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    payload = {
        "model": "gpt-4.1",
        "messages": messages,
        "max_tokens": 180
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        data = response.json()
        return data["choices"][0]["message"]["content"]
