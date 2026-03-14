import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)


load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
LANGFLOW_API_KEY = os.getenv("LANGFLOW_API_KEY")
LANGFLOW_URL = os.getenv("LANGFLOW_URL")


def split_text(text, chunk_size=4000):
    for i in range(0, len(text), chunk_size):
        yield text[i:i+chunk_size]

def send_to_langflow(message: str, file_path: str = None):
        headers = {"x-api-key": LANGFLOW_API_KEY}

        json_data = {
            "input_type": "chat",
            "output_type": "chat",
            "input_value": message,
        }
        headers["Content-Type"] = "application/json"
        response = requests.post(LANGFLOW_URL, headers=headers, json=json_data)

        try:
            response.raise_for_status()
            data = response.json()
            text = data["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            return text.replace("Text:", "").strip()
        except Exception as e:
            return f"Ошибка при обращении к API: {e}"
   

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
    """
    Привет! Я - ассистент маркетплейса
    """
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_text = update.message.text
        reply = send_to_langflow(user_text)
        for chunk in split_text(reply):
            await update.message.reply_text(chunk)
   

def main():
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .connect_timeout(30.0)
        .read_timeout(60.0)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()

