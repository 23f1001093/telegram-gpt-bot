import requests
from src.config import TELEGRAM_BOT_TOKEN, WEBHOOK_URL


response = requests.post(
    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook",
    data={"url": WEBHOOK_URL}
)
print(response.text)