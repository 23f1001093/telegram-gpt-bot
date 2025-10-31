import os
import httpx

DEFAULT_MODEL = "openai/gpt-oss-20b"
DEFAULT_SYSTEM_PROMPT = "AI Telegram bot."
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 200
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

async def get_gpt_reply(messages):
    api_key = os.getenv("OPENROUTER_API_KEY")   
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is not set in environment variables")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://d8b106d01091.ngrok-free.app"
 
    }

    payload = {
        "model": DEFAULT_MODEL,
        "messages": messages,
        "max_tokens": DEFAULT_MAX_TOKENS,
        "temperature": DEFAULT_TEMPERATURE,
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(OPENROUTER_API_URL, headers=headers, json=payload)
        resp.raise_for_status()
        result = resp.json()

    try:
        return result["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise RuntimeError(f"Bad response from OpenRouter: {result}")
