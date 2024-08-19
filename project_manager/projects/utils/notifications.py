import os
import requests
from django.conf import settings

def send_telegram_message(message):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    # bot_token = 'enter your token'
    # chat_id = 'enter chat id'
    api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    
    payload = {
        'chat_id': chat_id,
        'text': message,
    }
    response = requests.post(api_url, data=payload)
    response.raise_for_status()  # Raise an error if the request failed
