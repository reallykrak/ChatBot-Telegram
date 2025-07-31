import telebot
import requests

# BOT TOKEN VE API KEY
BOT_TOKEN = '8456728583:AAGVjaFzVdCrZuXSNrL7w0OQucdaZpYqmI0'
OPENROUTER_API_KEY = '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'  # BURAYA kendi OpenRouter API anahtarını yaz

# MODEL ADI
MODEL = 'deepseek-chat'  # OpenRouter destekli bir model (GPT-3.5 benzeri)

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text

    # OpenRouter API'ye istek ver
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourproject.example",  # Optional ama bazı modeller için gerekli
        "X-Title": "TelegramBot"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Sen bir Telegram sohbet botusun."},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                                 headers=headers,
                                 json=payload)

        if response.status_code == 200:
            data = response.json()
            reply = data["choices"][0]["message"]["content"]
            bot.reply_to(message, reply)
        else:
            bot.reply_to(message, f"API hatası: {response.status_code}")
    except Exception as e:
        bot.reply_to(message, f"Hata oluştu: {e}")

bot.polling()
