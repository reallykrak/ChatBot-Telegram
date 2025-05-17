import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# === BURAYA KENDİ BİLGİLERİNİ YAZ ===
TELEGRAM_TOKEN = "7763395301:AAF3thVNH883Rzmz0RTpsx3wuiCG_VLpa-g"
OPENROUTER_API_KEY = "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"

# === LOG AYARI ===
logging.basicConfig(level=logging.INFO)

# === /start KOMUTU ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! Ben ChatGPT botuyum. Bana bir şeyler yaz, cevap vereyim.")

# === MESAJ YÖNLENDİRME ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.chat.send_action(action="typing")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "X-Title": "TelegramChatGPTBot"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",  # Ücretsiz ve çalışan model
        "messages": [
            {"role": "system", "content": "Kısa, anlaşılır ve Türkçe cevaplar ver."},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        bot_reply = result['choices'][0]['message']['content']
        await update.message.reply_text(bot_reply)
    except requests.exceptions.HTTPError as e:
        await update.message.reply_text("API hatası: Anahtar geçersiz veya erişim yok (401 olabilir).")
    except Exception as e:
        await update.message.reply_text(f"Bir hata oluştu: {str(e)}")

# === BOTU ÇALIŞTIR ===
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot çalışıyor... Telegram'dan mesaj gönderebilirsin.")
    app.run_polling()

if __name__ == "__main__":
    main()
