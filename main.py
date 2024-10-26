import json
import telebot
import threading
from telebot import types
from keyboards import *

with open("config.json", 'r') as f:
    data = json.load(f)

training = False
bot = telebot.TeleBot(data["BotAPI"])

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я тестовый вариант бота для тестового занятия по фитнесу.\nКакая тренировка была бы тебе интересна?", reply_markup=fitness_workout())
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.register_next_step_handler(message, start_workout)

@bot.message_handler(content_types=["text"])
def start_workout(message):
    global training
    if message.text == "Стоп":
        if not training:
            bot.send_message(message.chat.id, "Тренировка не начата, выбери тренировку из списка", reply_markup=fitness_workout())
            return
        training = False
        bot.send_message(message.chat.id, "Тренировка окончена", reply_markup=fitness_workout())
        bot.send_message(message.chat.id, "Доступ к более подробным тренировкам вы можете преобрести у @Samsonova8", reply_markup=fitness_workout())
    elif message.text == "Пресс":
        if training:
            bot.send_message(message.chat.id, "Тренировка уже идет, остановить тренировку?", reply_markup=stop_workout())
            return
        bot.send_message(message.chat.id, "Начинаем тренировку для пресса", reply_markup=stop_workout())
        training = True
        threading.Thread(target=press_workout, args=(message,)).start()
    elif message.text == "Спина":
        if training:
            bot.send_message(message.chat.id, "Тренировка уже идет, остановить тренировку?", reply_markup=stop_workout())
            return
        bot.send_message(message.chat.id, "Начинаем тренировку для спины", reply_markup=stop_workout())
        training = True
        threading.Thread(target=back_workout, args=(message,)).start()
    elif message.text == "Ноги":
        if training:
            bot.send_message(message.chat.id, "Тренировка уже идет, остановить тренировку?", reply_markup=stop_workout())
            return
        bot.send_message(message.chat.id, "Начинаем тренировку для ног", reply_markup=stop_workout())
        training = True
        threading.Thread(target=legs_workout, args=(message,)).start()
    else:
        bot.send_message(message.chat.id, "Хм... Не знаю еще такой🫢. Пока что выбери тренировку из списка", reply_markup=fitness_workout())
    
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.register_next_step_handler(message, start_workout)

def press_workout(message):
    global training
    for i in data["press_workout"]:
        if not training:
            return
        bot.send_message(message.chat.id, "Видео с тренировкой для пресса")
        threading.Event().wait(data["sleep_time"])
    training = False

def back_workout(message):
    global training
    for i in data["back_workout"]:
        if not training:
            return
        bot.send_message(message.chat.id, "Видео с тренировкой для спины")
        threading.Event().wait(data["sleep_time"])
    training = False

def legs_workout(message):
    global training
    for i in data["legs_workout"]:
        if not training:
            return
        bot.send_message(message.chat.id, "Видео с тренировкой для ног")
        threading.Event().wait(data["sleep_time"])
    training = False

bot.polling(non_stop=True)
