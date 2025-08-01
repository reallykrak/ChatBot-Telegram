import telebot
import requests

BOT_TOKEN = '8456728583:AAGVjaFzVdCrZuXSNrL7w0OQucdaZpYqmI0'
GEMINI_API_KEY = 'AIzaSyDGXakapXgul46kbkC6P4RI-yObnzeFsgM'  # Kendi API anahtarınız

bot = telebot.TeleBot(BOT_TOKEN)

# Webhook'u devre dışı bırak (409 hatasını önler)
bot.remove_webhook()

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

# Bot'u başlat
bot.infinity_polling()
