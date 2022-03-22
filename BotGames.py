import requests
import random
#------
#___________________________________________________________________
class Hand:
    emo_ROCK = "U000270A"  # Unicod эмоджи Камень
    emo_PAPER = "U000270B"  # Unicod эмоджи Бумага
    emo_SCISSORS = "U000270C"  # Unicod эмоджи Ножницы
#___________________________________________________________________

def game(message):
    choice = random.choice(['Камень🤜', 'Ножницы✌️', 'Бумага✋'])
    if message.text == choice:
        bot.send_message(message.chat.id, 'Боевая ничья! Для начала новой игры пишите /start')
    else:
        if message.text == 'Камень🤜':
            if choice == 'Ножницы✌️':
                bot.send_message(message.chat.id,
                                 'Поздравляю с победой! У меня была {}. Для начала новой игры пишите /start'.format(
                                     choice))
            else:
                bot.send_message(message.chat.id,
                                 'Извените1, но Вы проиграли 😢. У меня был(и/a) {}. Для начала новой игры пишите /start'.format(
                                     choice))
        elif message.text == 'Ножницы✌️':
            if choice == 'Бумага✋':
                bot.send_message(message.chat.id,
                                 'Поздравляю с победой! У меня была {}. Для начала новой игры пишите /start'.format(
                                     choice))
            else:
                bot.send_message(message.chat.id,
                                 'Извените, но Вы проиграли 😢. У меня был(и/a) {}. Для начала новой игры пишите /start'.format(
                                     choice))
        elif message.text == 'Бумага✋':
            if choice == 'Камень🤜':
                bot.send_message(message.chat.id,
                                 'Поздравляю с победой! У меня была {}. Для начала новой игры пишите /start'.format(
                                     choice))
            else:
                bot.send_message(message.chat.id,
                                 'Извените, но Вы проиграли 😢. У меня был(и/a) {}. Для начала новой игры пишите /start'.format(
                                     choice))


# -----------------------------------------------------------------------
class Card:
    emo_SPADES = "U0002660"  # Unicod эмоджи Пики
    emo_CLUBS = "U0002663"  # Unicod эмоджи Крести
    emo_HEARTS = "U0002665"  # Unicod эмоджи Черви
    emo_DIAMONDS = "U0002666"  # Unicod эмоджи Буби

    def __init__(self, card):
        if isinstance(card, dict):  # если передали словарь
            self.__card_JSON = card
            self.code = card["code"]
            self.suit = card["suit"]
            self.value = card["value"]
            self.cost = self.get_cost_card()
            self.color = self.get_color_card()
            self.__imagesPNG_URL = card["images"]["png"]
            self.__imagesSVG_URL = card["images"]["svg"]

        elif isinstance(card, str):  # карту передали строкой, в формате "2S"
            self.__card_JSON = None
            self.code = card

            value = card[0]
            if value == "J":
                self.value = "JACK"
            elif value == "Q":
                self.value = "QUEEN"
            elif value == "K":
                self.value = "KING"
            elif value == "A":
                self.value = "ACE"
            elif value == "J":
                self.value = "JACK"
            else:
                self.value = value

            suit = card[1]
            if suit == "S":
                self.suit = "SPADES"  # Пики
            elif suit == "C":
                self.suit = "CLUBS"  # Крести
            elif suit == "H":
                self.suit = "HEARTS"  # Черви
            elif suit == "D":
                self.suit = "DIAMONDS"  # Буби

            self.cost = self.get_cost_card()
            self.color = self.get_color_card()

    def get_cost_card(self):
        if self.value == "JACK":
            return 2
        elif self.value == "QUEEN":
            return 3
        elif self.value == "KING":
            return 4
        elif self.value == "ACE":
            return 11
        elif self.value == "JOKER":
            return 1
        else:
            return int(self.value)

    def get_color_card(self):
        if self.suit == "SPADES":  # Пики
            return "BLACK"
        elif self.suit == "CLUBS":  # Крести
            return "BLACK"
        elif self.suit == "HEARTS":  # Черви
            return "RED"
        elif self.suit == "DIAMONDS":  # Буби
            return "RED"


# -----------------------------------------------------------------------
class Game21:
    def __init__(self, deck_count=1):
        new_pack = self.new_pack(deck_count)  # в конструкторе создаём новую пачку из deck_count-колод
        if new_pack is not None:
            self.pack_card = new_pack  # сформированная колода
            self.remaining = new_pack["remaining"],  # количество оставшихся карт в колоде
            self.card_in_game = []  # карты в игре
            self.arr_cards_URL = []  # URL карт игрока
            self.score = 0  # очки игрока
            self.status = None  # статус игры, True - игрок выиграл, False - Игрок проиграл, None - Игра продолжается

    # ---------------------------------------------------------------------
    def new_pack(self, deck_count):
        response = requests.get(f"https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count={deck_count}")
        # создание стопки карт из "deck_count" колод по 52 карты
        if response.status_code != 200:
            return None
        pack_card = response.json()
        return pack_card

    # ---------------------------------------------------------------------
    def get_cards(self, card_count=1):
        if self.pack_card == None:
            return None
        if self.status != None:  # игра закончена
            return None

        deck_id = self.pack_card["deck_id"]
        response = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={card_count}")
        # достать из deck_id-колоды card_count-карт
        if response.status_code != 200:
            return False

        new_cards = response.json()
        if new_cards["success"] != True:
            return False
        self.remaining = new_cards["remaining"]  # обновим в классе количество оставшихся карт в колоде

        arr_newCards = []
        for card in new_cards["cards"]:
            card_obj = Card(card)  # создаем объекты класса Card и добавляем их в список карт у игрока
            arr_newCards.append(card_obj)
            self.card_in_game.append(card_obj)
            self.score = self.score + card_obj.cost
            self.arr_cards_URL.append(card["image"])

        if self.score > 21:
            self.status = False
            text_game = "Очков: " + str(self.score) + " ВЫ ПРОИГРАЛИ!"

        elif self.score == 21:
            self.status = True
            text_game = "ВЫ ВЫИГРАЛИ!"
        else:
            self.status = None
            text_game = "Очков: " + str(self.score) + " в колоде осталось карт: " + str(self.remaining)

        return text_game


# -----------------------------------------------------------------------
if __name__ == "__main__":
    print("Этот код должен использоваться ТОЛЬКО в качестве модуля!")