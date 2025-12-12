import telebot
import os
from dotenv import load_dotenv
from openai import OpenAI

# загружаем .env
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in .env")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env")

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_story(prompt: str) -> str:
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
        "Привет! ✨\nНапиши тему или жанр — я сгенерирую историю."
    )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot.send_message(message.chat.id, "Генерирую историю...")
        story = generate_story(message.text)
        bot.send_message(message.chat.id, story)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")


print("Бот запущен. Нажми Ctrl+C для остановки.")
bot.infinity_polling()