import httpx
from src.config import TELEGRAM_BOT_TOKEN

async def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)
