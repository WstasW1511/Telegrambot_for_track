import os
import time
from configparser import ConfigParser
import pyautogui
import pygetwindow as pg
import time
import telebot
from datetime import datetime
import db
import json


config = ConfigParser()
config.read('./config.ini')
config = config._sections
token = config['system']['token']

bot = telebot.TeleBot(str(token)) #token bot
status = True


def log(message):
    print(" ------------")
    print(datetime.now())
    print("Сообщение от {0} {1}. (id = {2}) \n Текст - {3}".format(message.from_user.first_name,
                                                                   message.from_user.last_name,
                                                                   str(message.from_user.id),
                                                                   message.text))


def send_mess(message, status):
    if status != False:
        while True:
            time.sleep(1)
            try:
                send = json.loads(db.get_message_for_send(message.from_user.id))
                if send != "no":
                    bot.send_message(message.from_user.id, send['message'] + " Дата: " + send['datetime'])
            except:
                pass
    else:
        bot.send_message(message.from_user.id, "The end")


@bot.message_handler(commands=["start"])
def handle_start(message):
    log(message)
    bot.send_message(message.from_user.id, 'Добро пожаловать')
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/start', '/stop', )  # добавляем команды
    msg = bot.send_message(message.from_user.id, 'Введите Логин:', reply_markup=user_markup)
    bot.register_next_step_handler(msg, login)


def login(message):
    login = message.text
    msg = bot.send_message(message.from_user.id, 'Введите пароль:')
    bot.register_next_step_handler(msg, password, login)


def password(message, login):
    password = message.text
    data = {
        'login': login,
        'password': password,
        'user_id_message': message.from_user.id,
    }
    data = json.dumps(data)
    result = db.login(data)
    try:
        result = json.loads(result)
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Получать данные', 'Выход', 'Скриншот')
        msg = bot.send_message(message.from_user.id, 'Здравтствуйте %s'% result['name'], reply_markup=user_markup)
    except:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('/start', '/stop', )
        msg = bot.send_message(message.from_user.id, '%s нажмите старт' % result, reply_markup=user_markup)


@bot.message_handler(commands=["stop"])
def handle_start(message):  # функция, которая убирает нашу клавиатуру
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, '...', reply_markup=hide_markup)
    db.status_to_send(message.from_user.id, status=False)
    send_mess(message, status=False)
    log(message)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    log(message)
    if message.text == 'Получать данные':
        db.status_to_send(message.from_user.id, status=True)
        send_mess(message, status=True)
        bot.send_message(message.from_user.id, db.get_message_for_send(message.from_user.id))
    elif message.text == 'Скриншот':
        screen = pyautogui.screenshot('screenshot.png')
        img = open('screenshot.png', 'rb')
        bot.send_photo(message.from_user.id, img)
    elif message.text == 'Выход':
        db.status_to_send(message.from_user.id, status=False)
        send_mess(message, status=False)
        hide_markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, '...')
bot.polling(none_stop=True, interval=0)

