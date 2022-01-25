import telebot

token = open('token.txt').readline().rstrip()
bot = telebot.TeleBot(token)

# /start
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "У аппарата ...")

# Return message back
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, "Echo: " + message.text)

# Polling messages
bot.infinity_polling()
