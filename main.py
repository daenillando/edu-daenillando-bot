import telebot
import os
from sql.sql import Database

with open('token.txt') as file:
    token = file.readline().rstrip()
bot = telebot.TeleBot(token)
if not os.path.exists("./chats"):
    print("making folder")
    os.mkdir("chats")
chats = {}
for filename in os.listdir("./chats"):
    chat_id = int(filename[5:-3])
    chats[chat_id] = Database("./chats/" + filename)

# /start
@bot.message_handler(commands = ["start"])
def start(message):
    if not message.chat.id in chats:
        chats[message.chat.id] = Database("./chats/chat_{0}.db".format(message.chat.id))
    bot.send_message(message.chat.id, "У аппарата ...")

@bot.message_handler(commands = ["add"])
def add(message):
    category, name, price = message.text.split(' ')[1:4]
    chats[message.chat.id].c_add(category, name, price)

@bot.message_handler(commands = ["remove"])
def remove(message):
    id = message.text.split(' ')[1]
    chats[message.chat.id].c_remove(id)

@bot.message_handler(commands = ["list"])
def list(message):
    parsed = message.text.split(' ')
    if len(parsed) > 1:
        category = parsed[1]
    else:
        category = None
    text = "ID\tДата\tКатегория\tНаименование\tЦена, руб\n"
    for row in chats[message.chat.id].c_list(category):
        for field in row:
            text += str(field) + "\t"
        text += "\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands = ["sum"])
def sum(message):
    bot.send_message(message.chat.id, "Всего потрачено: {0} рублей".format(chats[message.chat.id].c_sum()))

# Return message back
@bot.message_handler(content_types = ["text"])
def handle_text(message):
    bot.send_message(message.chat.id, "Такой команды не знаю: " + message.text)

# Polling messages
bot.infinity_polling()
