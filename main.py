import os
import openai
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
PROMPT_ID = os.getenv("PROMPT_ID")
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
YANDEX_PROJECT_ID = os.getenv("YANDEX_PROJECT_ID")

client = openai.OpenAI(
    api_key=YANDEX_API_KEY,
    base_url="https://rest-assistant.api.cloud.yandex.net/v1",
    project=YANDEX_PROJECT_ID,
)


def ask_yandex_stream(user_message: str):
    """
    Возвращает генератор, который yield'ит куски текста от YandexGPT
    """
    stream = client.responses.stream(
        model=f"gpt://{YANDEX_PROJECT_ID}/yandexgpt/rc",
        prompt={"id": PROMPT_ID},
        input=user_message,
    )
    return stream


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
Привет! Я — финансовый эксперт, контент-мейкер и редактор соцсетей, помогу написать тебе статью
        """
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    sent_msg = await update.message.reply_text("Генерирую ответ...")

    full_text = ""

    with ask_yandex_stream(user_text) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                delta = event.delta
                full_text += delta
        
                try:
                    await sent_msg.edit_text(full_text)
                except:
                    pass
    return


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

    print("Бот запущен!")
    try:
        app.run_polling()
    except KeyboardInterrupt:
        print("Бот остановлен")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()