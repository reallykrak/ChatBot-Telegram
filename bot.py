import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Anahtarları buraya gir
TELEGRAM_TOKEN = '7763395301:AAF3thVNH883Rzmz0RTpsx3wuiCG_VLpa-g'  # BotFather'dan aldığın token
OPENROUTER_API_KEY = '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'

# Logging (isteğe bağlı)
logging.basicConfig(level=logging.INFO)

# Başlangıç komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! Ben ChatGPT botuyum. Bana mesaj yazarak sohbet edebilirsin.")

# Mesajlara cevap
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.chat.send_action(action="typing")

    # OpenRouter API isteği
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_message}]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        bot_reply = response.json()['choices'][0]['message']['content']
        await update.message.reply_text(bot_reply)
    except Exception as e:
        await update.message.reply_text(f"Hata oluştu: {str(e)}")

# Botu çalıştır
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("DevReallykrak")
    app.run_polling()

if __name__ == '__main__':
    main()
