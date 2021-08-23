from telebot import TeleBot

def init(token, user_id):
    bot = TeleBot(token)
    return bot