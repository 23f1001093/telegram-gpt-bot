from fastapi import FastAPI, Request, Header
from src.ai_model import get_gpt_reply
from src.telegram_api import send_message , send_message_with_keyboard, reply_options_keyboard_json, send_voice_message
from src.config import WEBHOOK_SECRET
from dotenv import load_dotenv
from src.routes import api_router
load_dotenv()
import os
print("Loaded OPENROUTER_API_KEY:", os.getenv("OPENROUTER_API_KEY"))

last_bot_reply = {}

app = FastAPI()

app.include_router(api_router)

@app.post("/webhook")
async def telegram_webhook(request: Request, x_secret: str = Header(None)):
    print("=" * 40)
    print("Webhook POST received")
    
    #if WEBHOOK_SECRET and x_secret != WEBHOOK_SECRET:
     #   print("Invalid secret! Got:", x_secret)
       # return {"error": "Invalid secret"}

    try:
        update = await request.json()
        if "callback_query" in update:
            callback = update["callback_query"]
            chat_id = callback["message"]["chat"]["id"]
            data = callback["data"]
            if data == "get_voice_reply":
                reply_text = last_bot_reply.get(chat_id, "Sorry, no reply found.")
                await send_voice_message(chat_id, reply_text)
                await send_message(chat_id, "Voice reply sent! 🎤")
                return {"ok": True}


        print("Update payload:", update)
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        user_text = message.get("text")
        print("Chat ID:", chat_id, "User text:", user_text)

        if chat_id and user_text:
            messages = [
                {"role": "system", "content": "You are a helpful AI Telegram bot."},
                {"role": "user", "content": user_text}
            ]
            try:
                reply = await get_gpt_reply(messages)
                print("GPT reply:", reply)
                await send_message(chat_id, reply)
                print("Reply sent to Telegram.")
                last_bot_reply[chat_id] = reply
                await send_message_with_keyboard(chat_id, "Want to hear this reply as voice?", reply_options_keyboard_json)

                print("Reply sent to Telegram.")
            except Exception as e:
                print("Error calling GPT or sending Telegram message:", e)
        else:
            print("No chat_id or user_text in incoming message.")

    except Exception as ex:
        print("Error processing webhook payload:", ex)

    print("=" * 40)
    return {"ok": True}