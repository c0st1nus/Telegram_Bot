from telebot import types

def fitness_workout():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("Пресс", "Спина", "Ноги", "Стоп")
    return markup

def stop_workout():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("Стоп")
    return markup