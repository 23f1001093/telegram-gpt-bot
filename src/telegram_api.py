import httpx
from src.config import TELEGRAM_BOT_TOKEN
from gtts import gTTS
import os
import json
async def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

async def send_message_with_keyboard(chat_id, text, keyboard_json):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": keyboard_json
    }
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

async def send_voice_message(chat_id, text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    mp3_path = 'temp_voice.mp3'
    ogg_path = 'temp_voice.ogg'
    tts.save(mp3_path)

    # Convert mp3 to ogg/opus for Telegram
    import subprocess
    subprocess.run(['ffmpeg', '-y', '-i', mp3_path, '-c:a', 'libopus', ogg_path], check=True)

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVoice"
    async with httpx.AsyncClient() as client:
        with open(ogg_path, 'rb') as f:
            data = {"chat_id": chat_id}
            files = {"voice": f}
            await client.post(url, data=data, files=files)

    # Clean up temp files
    os.remove(mp3_path)
    os.remove(ogg_path)


reply_options_keyboard = {
    "inline_keyboard": [
        [
            {"text": "🎤 Get Voice Reply", "callback_data": "get_voice_reply"}
        ]
    ]
}
reply_options_keyboard_json = json.dumps(reply_options_keyboard)
