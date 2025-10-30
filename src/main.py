from fastapi import FastAPI, Request, Header
from src.ai_model import get_gpt_reply
from src.telegram_api import send_message
from src.config import WEBHOOK_SECRET

app = FastAPI()

@app.post("/webhook")
async def telegram_webhook(request: Request, x_secret: str = Header(None)):
    if WEBHOOK_SECRET and x_secret != WEBHOOK_SECRET:
        return {"error": "Invalid secret"}
    update = await request.json()
    message = update.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    user_text = message.get("text")
    if chat_id and user_text:
        
        messages = [
            {"role": "system", "content": "You are a helpful AI Telegram bot."},
            {"role": "user", "content": user_text}
        ]
        reply = await get_gpt_reply(messages)
        await send_message(chat_id, reply)
    return {"ok": True}
