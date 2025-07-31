import telebot
import requests

BOT_TOKEN = '8456728583:AAGVjaFzVdCrZuXSNrL7w0OQucdaZpYqmI0'
GEMINI_API_KEY = 'AIzaSyDGXakapXgul46kbkC6P4RI-yObnzeFsgM'  # BURAYA kendi Google API anahtarını yapıştır

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text

    try:
        url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}'

        payload = {
            "contents": [
                {"parts": [{"text": user_input}]}
            ]
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            reply = response.json()['candidates'][0]['content']['parts'][0]['text']
            bot.reply_to(message, reply)
        else:
            bot.reply_to(message, f"API hatası: {response.status_code} - {response.text}")

    except Exception as e:
        bot.reply_to(message, f"Hata oluştu: {e}")

bot.polling()
