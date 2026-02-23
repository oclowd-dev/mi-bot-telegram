import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Leer claves desde variables de entorno
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise ValueError("Faltan variables de entorno TELEGRAM_TOKEN o GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        mensaje = update.message.text
        respuesta = model.generate_content(mensaje)
        await update.message.reply_text(respuesta.text)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

print("✅ Bot iniciado. Envíale un mensaje en Telegram...")
app.run_polling()
