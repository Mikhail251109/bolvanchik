import telebot
import os
from dotenv import load_dotenv
from openai import OpenAI
from database import init_db, save_story

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in .env")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env")


bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)


init_db()
print("База данных инициализирована")


def generate_story(prompt: str) -> str:
    """
    Генерация истории через OpenAI
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты генератор коротких художественных историй."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! ✨\n"
        "Напиши тему или жанр — я сгенерирую историю.\n\n"
        "Пример:\n"
        "👉 Фэнтези про дракона и мага"
    )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_message(message.chat.id, "Генерирую историю... ⏳")

    try:
        prompt = message.text
        story = generate_story(prompt)

        # Сохраняем в базу данных
        save_story(
            user_id=message.from_user.id,
            username=message.from_user.username,
            prompt=prompt,
            story=story
        )

        bot.send_message(message.chat.id, story)

    except Exception as e:
        print("Ошибка:", e)
        bot.send_message(
            message.chat.id,
            "❌ Произошла ошибка при генерации истории. Попробуй позже."
        )


print("Бот запущен. Нажми Ctrl+C для остановки.")
bot.infinity_polling()
