import telebot
import os

#Токен и создание бота TG
token = ""
bot = telebot.TeleBot(token)


#Блок данных для авторизации в БД

connect_db = ["localhost", "", "", ""]

#Базовый путь к изображениям
base_card_dir = "/tmp/cards/"
#Названия файлов изображений
cards = os.listdir("." + base_card_dir)
