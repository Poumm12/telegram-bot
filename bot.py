import telebot
from telebot import types
from config import TOKEN
from database import init_db, add_user, get_user

bot = telebot.TeleBot(TOKEN)

# Αρχικοποίηση βάσης δεδομένων
init_db()

@bot.message_handler(commands=['start'])
def start(message):
    user = get_user(message.chat.id)
    if not user:
        add_user(message.chat.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    
    bot.send_message(message.chat.id, f"👋 Καλώς ήρθες, {message.from_user.first_name}!\n\nΧρησιμοποίησε /menu για επιλογές.")

@bot.message_handler(commands=['menu'])
def menu(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📖 Προφίλ", "⚙️ Ρυθμίσεις", "ℹ️ Βοήθεια")
    bot.send_message(message.chat.id, "Επέλεξε μια επιλογή:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "📖 Προφίλ")
def profile(message):
    user = get_user(message.chat.id)
    if user:
        bot.send_message(message.chat.id, f"👤 Όνομα: {user[2]} {user[3]}\n💬 Username: @{user[1]}")
    else:
        bot.send_message(message.chat.id, "❌ Δεν βρέθηκαν στοιχεία.")

@bot.message_handler(func=lambda message: message.text == "⚙️ Ρυθμίσεις")
def settings(message):
    bot.send_message(message.chat.id, "🔧 Ρυθμίσεις (Σε ανάπτυξη...)")

@bot.message_handler(func=lambda message: message.text == "ℹ️ Βοήθεια")
def help_message(message):
    bot.send_message(message.chat.id, "❓ Είμαι ένα bot που αποθηκεύει χρήστες και παρέχει υπηρεσίες.")

print("🤖 Το bot είναι online!")
bot.polling()
