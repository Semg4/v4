
# Телеграм-бот v.004
import json

import telebot  # pyTelegramBotAPI 4.3.1
from telebot import types
import requests
import bs4
import BotGames  # бот-игры, файл BotGames.py
from menuBot import Menu  # в этом модуле есть код, создающий экземпляры классов описывающих моё меню
import DZ  # домашнее задание от первого урока


bot = telebot.TeleBot('5173440304:AAGOO6PhsDxOdKwCfpeOgHwPquwRd90jc3w')  # Создаем экземпляр бота
game21 = None  # класс игры в 21, экземпляр создаём только при начале игры

# -----------------------------------------------------------------------
# Функция, обрабатывающая команды
@bot.message_handler(commands="start")
def command(message, res=False):
    txt_message = "Привет, {message.from_user.first_name}! Я тестовый бот для курса программирования на языке Python"
    bot.send_message(message.chat.id, text=txt_message, reply_markup=Menu.getMenu("Главное меню").markup)


# -----------------------------------------------------------------------
# Получение сообщений от юзера
@bot.message_handler(content_types=['text1'])
def get_text_messages(message):
    global game21

    chat_id = message.chat.id
    ms_text = message.text

    result = goto_menu(chat_id, ms_text)  # попытаемся использовать текст как команду меню, и войти в него
    if result == True:
        return  # мы вошли в подменю, и дальнейшая обработка не требуется

    if Menu.cur_menu != None and ms_text in Menu.cur_menu.buttons: # проверим, что команда относится к текущему меню

        if ms_text == "Помощь":
            send_help(chat_id)

        elif ms_text == "Прислать кота" or ms_text == "/кот":
            bot.send_photo(chat_id, photo=get_catURL(), caption="Держи котика, не обижай его!")

        elif ms_text == "Прислать анекдот":
            bot.send_message(chat_id, text=get_anekdot())

        elif ms_text == "Прислать картинку":
            bot.send_message(chat_id, text=get_wtr())

        elif ms_text == "Карту!":
            if game21 == None:  # если мы случайно попали в это меню, а объекта с игрой нет
                goto_menu(chat_id, "Выход")
                return

            text_game = game21.get_cards(1)
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

            if game21.status != None:  # выход, если игра закончена
                goto_menu(chat_id, "Выход")
                return

        elif ms_text == "Камень, ножницы, бумага":
            if game_rsp == None:  # если мы случайно попали в это меню, а объекта с игрой нет
                goto_menu(chat_id, "Выход")
                return
            bot.send_message("Выбирай жест, чтобы начать игру")
            text_game = game_rsp.get_cards(1)
            bot.send_media_group(chat_id, media=getMediaCards(game_rsp))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

            if game_rsp.status != None:  # выход, если игра закончена
                goto_menu(chat_id, "Выход")
                return



        elif ms_text == "Стоп!":
            game21 = None
            goto_menu(chat_id, "Выход")
            return

        elif ms_text == "Задание-1":
            DZ.dz1(bot, chat_id)

        elif ms_text == "Задание-2":
            DZ.dz2(bot, chat_id)

        elif ms_text == "Задание-3":
            DZ.dz3(bot, chat_id)

        elif ms_text == "Задание-4":
            DZ.dz4(bot, chat_id)

        elif ms_text == "Задание-5":
            DZ.dz5(bot, chat_id)

        elif ms_text == "Имя":
            DZ.dz6(bot, chat_id)

    else:  # ...........................................................................................................
        bot.send_message(chat_id, text="Мне жаль, я не понимаю вашу команду: " + ms_text)
        goto_menu(chat_id, "Главное меню")
# -----------------------------------------------------------------------
def goto_menu(chat_id, name_menu):

    # получение нужного элемента меню
    if name_menu == "Выход" and Menu.cur_menu != None and Menu.cur_menu.parent != None:
        target_menu = Menu.getMenu(Menu.cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(name_menu)

    if target_menu != None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)

        # Проверим, нет ли обработчика для самого меню. Если есть - выполним нужные команды
        if target_menu.name == "Игра в 21":
            global game21
            game21 = BotGames.Game21()  # создаём новый экземпляр игры
            text_game = game21.get_cards(2)  # просим 2 карты в начале игры
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

        return True
    else:
        return False
# -----------------------------------------------------------------------
def getMediaCards(game21):
    medias = []
    for url in game21.arr_cards_URL:
        medias.append(types.InputMediaPhoto(url))
    return medias

# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
def get_anekdot():
    array_anekdots = []
    req_anek = requests.get('http://anekdotme.ru/random')
    soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
    result_find = soup.select('.anekdot_text')
    for result in result_find:
        array_anekdots.append(result.getText().strip())
    return array_anekdots[0]
#_______________________________________________________________________
def get_wtr():
    array_wtr = []
    req_wtr = requests.get('https://www.gismeteo.ru/')
    soup = bs4.BeautifulSoup(req_wtr.text(), "html.parser")
    result_find = soup.select('.unit unit_temperature_c')
    for result in result_find:
        array_wtr.append(result.getText().strip())
    result_find = soup.select('.weather-description')
    for result in result_find:
        array_wtr.append(result.getText().strip())
    return array_wtr[0,1]

# -----------------------------------------------------------------------
def get_catURL():
    contents = requests.get('https://genrandom.com/cats/.json').json()
    return contents['url']


# ---------------------------------------------------------------------
bot.polling(none_stop=True, interval=0)  # Запускаем бота

print()