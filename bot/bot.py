import telebot
from sqlalchemy import *
import threading
from models import Session, Passphrase, User
from schedulers import cleanupScheduler, articleScheduler
from parser import parse

bot = telebot.TeleBot("7480261080:AAE-fGxbhX5vVD71GcxYcrYhddcPE0v40Lg")

@bot.message_handler(content_types = ['text'])
def handle_message(message):
    command = parse(message.text)
    if command['command'] == '/verify' and command['quantity'] == 1:
        with Session() as session:
            phrase = session.query(Passphrase).filter(Passphrase.phrase == command['args'][0]).first()
            if not phrase:
                bot.send_message(message.from_user.id, "Неправильний пароль")
                return
        
            user = session.query(User).get(phrase.user)

            if user and user.telegramId != -1:
                bot.send_message(message.from_user.id, "Ваш профіль вже підтверждено")
                return
        
            user.telegramId = message.from_user.id

            session.add(user)
            session.commit()

            bot.send_message(message.from_user.id, "Профіль підтверджено успішно")


threading.Thread(target = cleanupScheduler, args = [60]).start()
threading.Thread(target = articleScheduler, args = [60, bot]).start()
bot.polling()
