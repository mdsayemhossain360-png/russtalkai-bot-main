import os
import random
import asyncio
from gtts import gTTS
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("8759923548:AAH011SnYXIOf589on-mzJl4wW6IbMXC-ws")  # Token must be set in Railway Variables

# Vocabulary
words = [
    ("Привет","privet","Hello"),
    ("Спасибо","spasiba","Thank you"),
    ("Друг","drug","Friend"),
    ("Дом","dom","House"),
    ("Книга","kniga","Book")
]

# Sentences
sentences = {
    "bus":[
        ("Где остановка автобуса?","gdye astanofka avtobusa","Where is the bus stop"),
        ("Сколько стоит билет?","skolka stoit bilyet","How much is the ticket"),
        ("Я хочу выйти здесь","ya khochu vyiti zdes","I want to get off here")
    ],
    "medical":[
        ("У меня болит голова","u menya balit galava","I have headache"),
        ("Мне нужна помощь врача","mnye nuzhna pomosh vracha","I need a doctor"),
        ("Где аптека","gdye apteka","Where is pharmacy")
    ],
    "restaurant":[
        ("Можно меню пожалуйста","mozhna menyu pazhalusta","Menu please"),
        ("Я хочу заказать","ya khochu zakazat","I want to order"),
        ("Счёт пожалуйста","schyot pazhalusta","Bill please")
    ],
    "supershop":[
        ("Сколько это стоит","skolka eto stoit","How much is this"),
        ("Где хлеб","gdye khleb","Where is bread"),
        ("Я хочу купить молоко","ya khochu kupit malako","I want to buy milk")
    ]
}

# Quiz
quiz_words = {
    "Спасибо":"thank you",
    "Привет":"hello",
    "Друг":"friend"
}

# Grammar
grammar_text = """
Verb: говорить (to speak)

Я говорю
Ты говоришь
Он говорит
Мы говорим
Вы говорите
Они говорят
"""

# ---------------- Handlers ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard=[
        [InlineKeyboardButton("🚌 Bus",callback_data="bus")],
        [InlineKeyboardButton("🏥 Medical",callback_data="medical")],
        [InlineKeyboardButton("🍽 Restaurant",callback_data="restaurant")],
        [InlineKeyboardButton("🛒 SuperShop",callback_data="supershop")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = """🇷🇺 RussTalk Bot
Commands:
/word
/dailyword
/quiz
/grammar
"""
    await update.message.reply_text(text, reply_markup=reply_markup)

async def word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    w = random.choice(words)
    text = f"🇷🇺 {w[0]}\n🔊 {w[1]}\n🇬🇧 {w[2]}"
    await update.message.reply_text(text)
    tts = gTTS(w[0], lang="ru")
    filename = "voice.mp3"
    tts.save(filename)
    await update.message.reply_audio(audio=open(filename,"rb"))
    os.remove(filename)

async def dailyword(update: Update, context: ContextTypes.DEFAULT_TYPE):
    w = random.choice(words)
    text = f"📅 Daily Word\n🇷🇺 {w[0]}\n🔊 {w[1]}\n🇬🇧 {w[2]}"
    await update.message.reply_text(text)

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = random.choice(list(quiz_words.keys()))
    context.user_data["answer"] = quiz_words[q]
    await update.message.reply_text(f"What is the meaning of:\n{q}")

async def grammar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(grammar_text)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data
    s = random.choice(sentences[category])
    text = f"🇷🇺 {s[0]}\n🔊 {s[1]}\n🇬🇧 {s[2]}"
    await query.edit_message_text(text)
    tts = gTTS(s[0], lang="ru")
    filename = "voice.mp3"
    tts.save(filename)
    await query.message.reply_audio(open(filename,"rb"))
    os.remove(filename)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "answer" in context.user_data:
        if update.message.text.lower() == context.user_data["answer"]:
            await update.message.reply_text("✅ Correct")
        else:
            await update.message.reply_text(f"❌ Wrong\nCorrect: {context.user_data['answer']}")

# ---------------- Main ----------------

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("word", word))
    app.add_handler(CommandHandler("dailyword", dailyword))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CommandHandler("grammar", grammar))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT, chat))
    print("Bot running...")
    await app.run_polling()

asyncio.run(main())
