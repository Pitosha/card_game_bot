import config as c
import random
import chat
import user
from time import sleep
from telebot import types

#Обработка первого появления Бота в чате
@c.bot.message_handler(content_types=['new_chat_members'])
def reg_chat(message):
    if message.new_chat_member.id == c.bot.get_me().id:
        #Вызываем класс Чат
        this_chat = chat.Chat(message.chat.id)
        #Проверяем БД на наличие чата с таким id
        check_chat = this_chat.init_chat("bool")

        #Если чата с таким id не существует
        if check_chat is False:
            #Регистрируем ЧАТ в БД
            this_chat.create_chat(message.chat.title, 0, 0, 0, 0, 0, 0, 0, 0)
            c.bot.send_photo(message.chat.id, open("tmp/main_card.png", "rb"), caption="Это игровой бот, повторяющий правила карточной игры 21 но. Стань чемпионом Telegram, одержи победы над самыми непобедимыми игроками.\n\nДля того что бы зарегистрироваться как игрок, просто нажми команду /start \n\nХочешь собственного Telegram бота? Обращайся по адресу @tony_rainbow_pony")

        elif check_chat is True:
            c.bot.send_message(message.chat.id, "Ваш чат уже зарегестрирован как игральная комната")

#Обработка первого появления Бота в чате
@c.bot.message_handler(content_types=['left_chat_member'])
def del_chat(message):
    if message.left_chat_member.id == c.bot.get_me().id:
        
        #Вызываем класс Чат
        this_chat = chat.Chat(message.chat.id)
    
        #Удаляем чат
        this_chat.delete_chat()

@c.bot.message_handler(commands=["start"])
def start(message):
    if message.chat.type == 'private':
        c.bot.send_message(message.from_user.id, "Эта команда работает только в чате")
    else:
        #Вызываем класс User
        this_user = user.User(message.from_user.id)
        #Проверяем юзера на существование в БД
        check_user = this_user.init_user("bool")

        #Если юзер не существует в БД то регистриуем его
        if check_user is False:
            this_user.create_user(message.from_user.first_name)
            c.bot.send_message(message.chat.id, "" + message.from_user.first_name + ", ты успешно зарегестрировали аккаунт игрока. Добро пожаловать!!!")
        elif check_user is True:
            c.bot.send_message(message.chat.id, "Аккаунт игрока уже зареган")

@c.bot.message_handler(commands=['endgame'])
def endgame(message):
    admins = c.bot.get_chat_administrators(message.chat.id)

    i = 0

    while i < len(admins):
        if admins[i].user.id == message.from_user.id:
            this_chat = chat.Chat(message.chat.id)
            check = this_chat.init_chat("obj")
            
            if check[2] != 0:

                if check[7] != 0:
                    try:
                        c.bot.delete_message(check[0], check[7])
                    except:
                        pass
                else:
                    pass

                this_chat.update_chat(check[1], 0, 0, 0, 0, 0, 0, 0, 0)

            else:
                pass

            break
        else:
            pass

        i += 1

        if i == len(admins):
            c.bot.send_message(message.chat.id, "Эта команда доступна только админу")

@c.bot.message_handler(commands=["help"])
def help(message):
    if message.chat.type == 'private':
        c.bot.send_message(message.from_user.id, "Эта команда работает только в чате")
    else:
        #Вызываем класс User
        this_user = user.User(message.from_user.id)
        #Проверяем юзера на существование в БД
        check_user = this_user.init_user("bool")

        if check_user is False:
            c.bot.send_message(message.chat.id, "" + message.from_user.first_name + ", у тебя не зарегестрирован аккаунт игрока. Для регистрации нажмите команду /start")
        elif check_user is True:
            c.bot.send_message(message.chat.id, "Это классическая игра в 21но. Всё как обычно, тянешь карты, считаешь очки, надеешься на удачу :) \n\nЕсли наберешь юольше 21 го - перебор. Если если по окончании игры у тебя очков больше чем у соперника, тебе начисляется 1 балл победы. К слову о балах:\n\n У каждого игрока есть графа побед и поражений, рейтинг будет составлятся на основании этих двух граф. Если у вас с кем то одинаковое количество очков,и вы не можите поделить рейтинговое место, то количество поражений каждого из вас, поможет рассудить ситуацию.\n\nПеред тем как начать игру, нужно зарегистрировать 'Аккаунт игрока'. Сделать это можно вызвав команду /start \n\nНа тот случай, если кто то начал играть и не доиграл, тем самым оставив висеть игру, не давайя возможность начать её заново, или же на случай других неполадкот, ТОЛЬКО ДЛЯ АДМИНОВ существует команда /endgame . Это команда аварийного завершения игры. Она обнуляет все значения игровой комнаты влияющие на игру. Притяной игры. \n\nХочешь собственного Telegram бота? Обращайся по адресу @tony_rainbow_pony")

@c.bot.message_handler(commands=["rating"])
def rating_messages(message):
    if message.chat.type == 'private':
        c.bot.send_message(message.from_user.id, "Эта команда работает только в чате")
    else:
        #Вызываем класс User
        this_user = user.User(message.from_user.id)
        #Проверяем юзера на существование в БД
        check_user = this_user.init_user("bool")

        if check_user is False:
            c.bot.send_message(message.chat.id, "" + message.from_user.first_name + ", у тебя не зарегестрирован аккаунт игрока. Для регистрации нажмите команду /start")
        elif check_user is True:
            #Строка рейтинга, которую мы будем набирать из следующего цыкла
            reit_string = ""
            #Выводим рейтинг игроков
            all_users = this_user.get_all_users()

            #сортируем массив игроков
            sorted_users = sorted(all_users, key=lambda win: (win[2], -win[3]),reverse=True)

            #Получаем обьект Юзера
            my_us = this_user.init_user("obj")
            #Получаем место юзера в списке игроков
            my_us_rang = sorted_users.index(my_us)
            #Финальное значение места нажавшего персонажа
            my_us_rang +=1

            #Прогоняем всех юзеров через цикл
            gamer_num = 0
            
            for i in sorted_users:
                if gamer_num != 10:
                    reit_string += "Имя игрока: " + str(i[1]) + "\nПобед: " + str(i[2]) + "\nПоражений: " + str(i[3]) + "\n\n"
                
                if gamer_num == 10:
                    break

                gamer_num += 1
            
            reit_string += "Ваше место в списке игроков: " + str(my_us_rang)



            c.bot.send_message(message.chat.id, "10 лучших игроков в Telegram\n\n" + reit_string)

@c.bot.message_handler(commands=["cardgame"])
def card_messages(message):
    if message.chat.type == 'private':
        c.bot.send_message(message.from_user.id, "Эта команда работает только в чате")
    else:
        this_user = user.User(message.from_user.id)
        check_user = this_user.init_user("bool")

        if check_user is False:
            c.bot.send_message(message.chat.id, "" + message.from_user.first_name + ", у тебя не зарегестрирован аккаунт игрока. Для регистрации нажмите команду /start")
        elif check_user is True:
            #Вызываем класс Чат
            this_chat = chat.Chat(message.chat.id)
            #Проверяем БД на наличие чата с таким id
            check_chat = this_chat.init_chat("obj")

            if check_chat[2] == 0:
                this_chat.update_chat(check_chat[1], 1, message.from_user.id, check_chat[4], check_chat[5], check_chat[6], check_chat[7], check_chat[8], check_chat[9])

                keyboard = types.InlineKeyboardMarkup(row_width=1)
                button = types.InlineKeyboardButton(text="Принять вызов", callback_data="game")
                keyboard.add(button)

                msg = c.bot.send_photo(message.chat.id, open("tmp/start_game.png", "rb"), caption="Игрок под ником " + str(message.from_user.first_name) + " запустил игру. Один из вас может принять его вызов", reply_markup=keyboard)

                i = 0
                while i < 10:
                    sleep(1)
                    i += 1

                if i == 10:
                    check = this_chat.init_chat("obj")
                    if check[2] != 2:
                        try:
                            c.bot.delete_message(check_chat[0], msg.message_id)
                            this_chat.update_chat(check_chat[1], 0, 0, 0, 0, 0, 0, 0, 0)
                        except:
                            pass
                    else:
                        pass

            elif check_chat[2] == 1:

                c.bot.send_message(message.chat.id, "Игра уже запущена, но у тебя еще есть шанс сесть за игровой стол, одно место ещё свободно")
            elif check_chat[2] == 2:

                c.bot.send_message(message.chat.id, "Игра уже запущена, и все места за игровым столом уже заняты. Подожди пока закончится игра в этом чате и сделай кому нибудь вызов")

#Обработка подтверждения игры
@c.bot.callback_query_handler(func=lambda call: call.data == "game")
def game_opponents(call):
    #Вызываем класс Чат
    this_chat = chat.Chat(call.message.chat.id)
    #Проверяем БД на наличие чата с таким id
    check_chat = this_chat.init_chat("obj")

    #Вызываем класс User
    this_user = user.User(call.from_user.id)
    #Проверяем юзера на существование в БД
    check_user = this_user.init_user("bool")

    if check_user is True:
        if check_chat[3] != call.from_user.id:
            this_chat.update_chat(check_chat[1], 2, check_chat[3], call.from_user.id, check_chat[5], check_chat[6], check_chat[7], check_chat[8], check_chat[9])
            c.bot.delete_message(call.message.chat.id, call.message.message_id)
            game(call.message.chat.id)
        else:
            msg = c.bot.send_message(call.message.chat.id, "Ты не можешь кинуть вызов самому себе")
            sleep(1)
            c.bot.delete_message(call.message.chat.id, msg.message_id)
    else:
        c.bot.send_message(call.message.chat.id, "" + call.from_user.first_name + ", у тебя не зарегестрирован аккаунт игрока. Для регистрации нажмите команду /start")

def game(chat_id):
    #Вызываем класс Чат
    this_chat = chat.Chat(chat_id)
    #Проверяем БД на наличие чата с таким id
    check_chat = this_chat.init_chat("obj")

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button_1 = types.InlineKeyboardButton(text="Взять карту", callback_data="add_card")
    button_2 = types.InlineKeyboardButton(text="Пасовать", callback_data="pas")
    keyboard.add(button_1, button_2)
    msg = c.bot.send_photo(chat_id, open("tmp/coloda.png", "rb"), caption="Игра запущена, в этом режиме вы можете братя карты набирая своё заветное 21но. Если вы решили что вам больше не нужно тянуть карты, нажмите кнопку 'ПАС'", reply_markup=keyboard)

    this_chat.update_chat(check_chat[1], check_chat[2], check_chat[3], check_chat[4], check_chat[5], check_chat[6], msg.message_id, check_chat[8], check_chat[9])

#Обработка взятие карты
@c.bot.callback_query_handler(func=lambda call: call.data == "add_card")
def add_card(call):
    #Вызываем класс Чат
    this_chat = chat.Chat(call.message.chat.id)
    #Проверяем БД на наличие чата с таким id
    check_chat = this_chat.init_chat("obj")

    if call.from_user.id == check_chat[3]:
        if check_chat[8] != 1:

            #Выбираем рандомную карту из массива в конфиг файле
            random_card = random.randint(1, 35)
            card_img_path = "." + c.base_card_dir + c.cards[random_card]
            card_item = init_card(c.cards[random_card])

            #Прибавляем очки набранной карты к очкам юзера
            this_user_item = check_chat[5] + card_item

            msg = c.bot.send_photo(check_chat[0], open(card_img_path, "rb"), caption="Игрок " + call.from_user.first_name + " вытащил карту\n\nНабрано очков: " + str(this_user_item))

            #обновляем чат, добавляю юзеру количество набранных очков
            this_chat.update_chat(check_chat[1], check_chat[2], check_chat[3], check_chat[4], this_user_item, check_chat[6], check_chat[7], check_chat[8], check_chat[9])

            sleep(2)
            c.bot.delete_message(call.message.chat.id, msg.message_id)

            if this_user_item > 21:
                this_chat.update_chat(check_chat[1], check_chat[2], check_chat[3], check_chat[4], this_user_item, check_chat[6], check_chat[7], 1, check_chat[9])

                #вызываем функция проверяющую готовность к окончанию игры
                get_result(check_chat[0])

        else:
            msg = c.bot.send_message(call.message.chat.id, "" + call.from_user.first_name + ", ты ПЕРЕБРАЛ, нажал ПАС, или набрал уже своё заветное 21но. Ожидай пока твой соперник не подтвердит свою готовность")
            sleep(2)
            c.bot.delete_message(call.message.chat.id, msg.message_id)


    elif call.from_user.id == check_chat[4]:
        if check_chat[9] != 1:

            #Выбираем рандомную карту из массива в конфиг файле
            random_card = random.randint(1, 35)
            card_img_path = "." + c.base_card_dir + c.cards[random_card]
            card_item = init_card(c.cards[random_card])

            #Прибавляем очки набранной карты к очкам юзера
            this_user_item = check_chat[6] + card_item

            msg = c.bot.send_photo(check_chat[0], open(card_img_path, "rb"), caption="Игрок " + call.from_user.first_name + " вытащил карту\n\nНабрано очков: " + str(this_user_item))

            #обновляем чат, добавляю юзеру количество набранных очков
            this_chat.update_chat(check_chat[1], check_chat[2], check_chat[3], check_chat[4], check_chat[5], this_user_item, check_chat[7], check_chat[8], check_chat[9])
            
            sleep(2)
            c.bot.delete_message(call.message.chat.id, msg.message_id)

            if this_user_item > 21:
                this_chat.update_chat(check_chat[1], check_chat[2], check_chat[3], check_chat[4], check_chat[5], this_user_item, check_chat[7], check_chat[8], 1)

                #вызываем функция проверяющую готовность к окончанию игры
                get_result(check_chat[0])
        else:
            msg = c.bot.send_message(call.message.chat.id, "" + call.from_user.first_name + ", ты ПЕРЕБРАЛ, нажал ПАС, или набрал уже своё заветное 21но. Ожидай пока твой соперник не подтвердит свою готовность")
            sleep(2)
            c.bot.delete_message(call.message.chat.id, msg.message_id)
    else:
        c.bot.send_message(call.message.chat.id, "Ты не учавствуешь в этой игре")

#Обработка кнопки ПАС
@c.bot.callback_query_handler(func=lambda call: call.data == "pas")
def pas(call):
    #Вызываем класс Чат
    this_chat = chat.Chat(call.message.chat.id)
    #Проверяем БД на наличие чата с таким id
    check_chat = this_chat.init_chat("obj")

    if call.from_user.id == check_chat[3]:
        if check_chat[8] != 1:
            this_chat.update_chat(check_chat[1], check_chat[2], check_chat[3], check_chat[4], check_chat[5], check_chat[6], check_chat[7], 1, check_chat[9])

            #вызываем функция проверяющую готовность к окончанию игры
            get_result(check_chat[0])
        else:
            msg = c.bot.send_message(check_chat[0], "Ты уже нажал ПАС")
            sleep(2)
            c.bot.delete_message(call.message.chat.id, msg.message_id)

    elif call.from_user.id == check_chat[4]:
        if check_chat[9] != 1:
            this_chat.update_chat(check_chat[1], check_chat[2], check_chat[3], check_chat[4], check_chat[5], check_chat[6], check_chat[7], check_chat[8], 1)

            #вызываем функция проверяющую готовность к окончанию игры
            get_result(check_chat[0])
        else:
            msg = c.bot.send_message(check_chat[0], "Ты уже нажал ПАС")
            sleep(2)
            c.bot.delete_message(call.message.chat.id, msg.message_id)
    else:
        c.bot.send_message(call.message.chat.id, "Ты не учавствуешь в этой игре")


def init_card(card):
    if card[0:1] == '1':
        return 10
    elif card[0:1] == '9':
        return 9
    elif card[0:1] == '8':
        return 8
    elif card[0:1] == '7':
        return 7
    elif card[0:1] == '6':
        return 6
    elif card[0:1] == 'J':
        return 2
    elif card[0:1] == 'K':
        return 4
    elif card[0:1] == 'Q':
        return 3
    elif card[0:1] == 'A':
        return 11

def get_result(chat_id):
    #Вызываем класс Чат
    this_chat = chat.Chat(chat_id)
    #Проверяем БД на наличие чата с таким id
    check_chat = this_chat.init_chat("obj")

    if check_chat[8] == 1 and check_chat[9] == 1:
        #Удаляем игровой стол
        c.bot.delete_message(check_chat[0], check_chat[7])

        #Инициализируем первого игрока
        first_user = user.User(check_chat[3])
        first = first_user.init_user("obj")

        #Инициализируем второго игрока
        second_user = user.User(check_chat[4])
        second = second_user.init_user("obj")

        if check_chat[5] > check_chat[6]:

            if check_chat[5] <= 21:

                message_text = "Игрок " + first[1] + " набрал " + str(check_chat[5]) + " очков\nИгрок " + second[1] + " набрал " + str(check_chat[6]) + " очков\n\nПобедил " + first[1] + "\n\nПроигравшему начисляется бал поражения, Победителю бал победы. Смотрите /rating"
                
                #Раздаем набранные очки юзерам
                first_user.update_user(first[1], first[2] + 1, first[3])
                second_user.update_user(second[1], second[2], second[3] + 1)

            elif check_chat[5] > 21 and check_chat[6] <= 21:

                message_text = "Игрок " + first[1] + " набрал " + str(check_chat[5]) + "(перебор) очков\nИгрок " + second[1] + " набрал " + str(check_chat[6]) + " очков\n\nПобедил " + second[1] + "\n\nПроигравшему начисляется бал поражения, Победителю бал победы. Смотрите /rating"

                #Раздаем набранные очки юзерам
                first_user.update_user(first[1], first[2], first[3] + 1)
                second_user.update_user(second[1], second[2] + 1, second[3])

            elif check_chat[5] > 21 and check_chat[6] > 21:

                message_text = "Игрок " + first[1] + " набрал " + str(check_chat[5]) + "(перебор) очков\nИгрок " + second[1] + " набрал " + str(check_chat[6]) + "(перебор) очков\n\nПобедителя нет" + "\n\nНикому ничего не начислится"

        elif check_chat[6] > check_chat[5]:

            if check_chat[6] <= 21:

                message_text = "Игрок " + first[1] + " набрал " + str(check_chat[5]) + " очков\nИгрок " + second[1] + " набрал " + str(check_chat[6]) + " очков\n\nПобедил " + second[1] + "\n\nПроигравшему начисляется бал поражения, Победителю бал победы. Смотрите /rating"

                #Раздаем набранные очки юзерам
                first_user.update_user(first[1], first[2], first[3] + 1)
                second_user.update_user(second[1], second[2] + 1, second[3])

            elif check_chat[6] > 21 and check_chat[5] <= 21:

                message_text = "Игрок " + first[1] + " набрал " + str(check_chat[5]) + " очков\nИгрок " + second[1] + " набрал " + str(check_chat[6]) + "(перебор) очков\n\nПобедил " + first[1] + "\n\nПроигравшему начисляется бал поражения, Победителю бал победы. Смотрите /rating"

                #Раздаем набранные очки юзерам
                first_user.update_user(first[1], first[2] + 1, first[3])
                second_user.update_user(second[1], second[2], second[3] + 1)

            elif check_chat[6] > 21 and check_chat[5] > 21:

                message_text = "Игрок " + first[1] + " набрал " + str(check_chat[5]) + "(перебор) очков\nИгрок " + second[1] + " набрал " + str(check_chat[6]) + "(перебор) очков\n\nПобедителя нет" + "\n\nНикому ничего не начислится"

        elif check_chat[6] == check_chat[5] or check_chat[5] == check_chat[6]:

            if check_chat[6] > 21:
                message_text = "Игрок " + first[1] + " набрал " + str(check_chat[5]) + "(перебор) очков\nИгрок " + second[1] + " набрал " + str(check_chat[6]) + "(перебор) очков\n\nПобедителя нет" + "\n\nНикому ничего не начислится"
            else:
                message_text = "Игрок " + first[1] + " набрал " + str(check_chat[5]) + " очков\nИгрок " + second[1] + " набрал " + str(check_chat[6]) + " очков\n\nПобедителя нет" + "\n\nНикому ничего не начислится"

        #Выводим сообщение с результатами
        msg = c.bot.send_photo(chat_id, open("tmp/finish_game.png", "rb"), caption=message_text)

        sleep(10)
        #Удаляем сообщение с результатами
        c.bot.delete_message(check_chat[0], msg.message_id)
        #Обнуляем счетчики игры
        this_chat.update_chat(check_chat[1], 0, 0, 0, 0, 0, 0, 0, 0)
    else:
        return False


if __name__ == "__main__":
    try:
        c.bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        print("чета не работает")
        sleep(20)