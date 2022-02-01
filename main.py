import telebot
from sql import database

with open('token.txt') as file:
    token = file.readline().rstrip()
bot = telebot.TeleBot(token)
db = database("sql_database.db")

# /start
@bot.message_handler(commands = ["start"])
def start(message):
    bot.send_message(message.chat.id, "У аппарата ...")

@bot.message_handler(commands = ["add"])
def add(message):
    category, name, price = message.text.split(' ')[1:4]
    db.add(category, name, price)

@bot.message_handler(commands = ["remove"])
def remove(message):
    id = message.text.split(' ')[1]
    db.remove(id)

@bot.message_handler(commands = ["list"])
def list(message):
    parsed = message.text.split(' ')
    if len(parsed) > 1:
        category = parsed[1]
    else:
        category = None
    text = "ID\tДата\tКатегория\tНаименование\tЦена, руб\n"
    for row in db.list(category):
        for field in row:
            text += str(field) + "\t"
        text += "\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands = ["sum"])
def sum(message):
    bot.send_message(message.chat.id, "Всего потрачено: {0} рублей".format(db.sum()))

# Return message back
@bot.message_handler(content_types = ["text"])
def handle_text(message):
    bot.send_message(message.chat.id, "Такой команды не знаю: " + message.text)

# Polling messages
bot.infinity_polling()
