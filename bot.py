import os
import random
import asyncio
from gtts import gTTS
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("8759923548:AAH011SnYXIOf589on-mzJl4wW6IbMXC-ws")  # Must set in Railway Variables

words = [
    ("Привет","privet","Hello"),
    ("Спасибо","spasiba","Thank you"),
    ("Друг","drug","Friend"),
    ("Дом","dom","House"),
    ("Книга","kniga","Book")
]

sentences = {
    "bus":[("Где остановка автобуса?","gdye astanofka avtobusa","Where is the bus stop")],
    "medical":[("У меня болит голова","u menya balit galava","I have headache")],
    "restaurant":[("Можно меню пожалуйста","mozhna menyu pazhalusta","Menu please")],
    "supershop":[("Сколько это стоит","skolka eto stoit","How much is this")]
}

async def generate_voice(text):
    filename = "voice.mp3"
    await asyncio.to_thread(lambda: gTTS(text, lang="ru").save(filename))
    return filename

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard=[
        [InlineKeyboardButton("🚌 Bus",callback_data="bus")],
        [InlineKeyboardButton("🏥 Medical",callback_data="medical")],
        [InlineKeyboardButton("🍽 Restaurant",callback_data="restaurant")],
        [InlineKeyboardButton("🛒 SuperShop",callback_data="supershop")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🇷🇺 RussTalk Bot\nChoose category", reply_markup=reply_markup)

async def word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    w = random.choice(words)
    await update.message.reply_text(f"🇷🇺 {w[0]}\n🔊 {w[1]}\n🇬🇧 {w[2]}")
    filename = await generate_voice(w[0])
    await update.message.reply_audio(open(filename,"rb"))
    os.remove(filename)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data
    s = random.choice(sentences[category])
    await query.edit_message_text(f"🇷🇺 {s[0]}\n🔊 {s[1]}\n🇬🇧 {s[2]}")
    filename = await generate_voice(s[0])
    await query.message.reply_audio(open(filename,"rb"))
    os.remove(filename)

async def main():
    app = Application.builder().token(8759923548:AAH011SnYXIOf589on-mzJl4wW6IbMXC-ws).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("word", word))
    app.add_handler(CallbackQueryHandler(button))
    print("Bot running...")
    await app.run_polling()

asyncio.run(main())
