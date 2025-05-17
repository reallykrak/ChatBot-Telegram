import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# GEREKLİ ANAHTARLARI BURAYA YAZ
TELEGRAM_TOKEN = '7763395301:AAF3thVNH883Rzmz0RTpsx3wuiCG_VLpa-g'
OPENROUTER_API_KEY = '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'

# Log sistemi
logging.basicConfig(level=logging.INFO)

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! Ben ChatGPT botuyum. Mesajını yaz, hemen cevaplayayım.")

# Kullanıcı mesajı geldiğinde
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.chat.send_action(action="typing")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "X-Title": "TelegramGPTBot"  # Bu header bazen zorunlu
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",  # ÜCRETSİZ MODEL
        "messages": [
            {"role": "system", "content": "Kısa ve net cevaplar ver."},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        bot_reply = response.json()['choices'][0]['message']['content']
        await update.message.reply_text(bot_reply)
    except Exception as e:
        await update.message.reply_text(f"Hata: {e}")

# Botu başlat
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot çalışıyor...")
    app.run_polling()

if __name__ == '__main__':
    main()
