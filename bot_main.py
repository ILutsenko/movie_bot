import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboardColor, VkKeyboardButton, VkKeyboard
import mysql.connector
import random
from bot_genres import category_list, list_of_genres
from datetime import datetime


def actors_producers_genres(film_id):
    selector_for_actors_func = ('SELECT * FROM actor_movie WHERE movie_id = %s')
    selector_for_producer_func = ('SELECT * FROM producer_movie WHERE movie_id = %s')
    selector_for_genres_func = ('SELECT * FROM genre_movie WHERE movie_id = %s')
    cursor.execute(selector_for_actors_func, (film_id, ))
    actors_func = cursor.fetchall()
    actors_func = [x[0] for x in actors_func]
    cursor.execute(selector_for_producer_func, (film_id, ))
    producer_func = cursor.fetchall()
    producer_func = [x[0] for x in producer_func]
    cursor.execute(selector_for_genres_func, (film_id, ))
    genres_func = cursor.fetchall()
    genres_func = [x[0] for x in genres_func]
    actor_line = ''
    producer_line = ''
    genres_line = ''
    for x in actors_func:
        selector_for_actors1 = ('SELECT * FROM actor WHERE id = %s')
        cursor.execute(selector_for_actors1, (x,))
        actor_in = cursor.fetchone()
        actor_line += f"{actor_in[1]}, "
    actor_line = actor_line[:-2]

    for y in producer_func:
        selector_for_producer1 = ('SELECT * FROM producer WHERE id = %s')
        cursor.execute(selector_for_producer1, (y,))
        producer_in = cursor.fetchone()
        producer_line += f"{producer_in[1]}, "

    for z in genres_func:
        selector_for_genres1 = ('SELECT * FROM genre WHERE id = %s')
        cursor.execute(selector_for_genres1, (z,))
        genre_in = cursor.fetchone()
        for key, value in list_of_genres.items():
            if value['code'] == genre_in[1]:
                genres_line += f"{value['Genre name']}, "

    producer_line = producer_line[:-2]
    actor_line = actor_line[:-2]
    genres_line = genres_line[:-2]
    line = [producer_line, actor_line, genres_line]
    return line


def get_connection():
    bot_db = mysql.connector.connect(
        user='root',
        passwd='a04011972',
        database='imdb_catalog',
        host='127.0.0.1'
    )
    return bot_db


def send_message(peer_id, message=None, attachment=None, keyboard=None, payload=None):
    vk.messages.send(peer_id=peer_id, message=message, random_id=random.randint(-2147483648, +2147483648),
                              attachment=attachment, keyboard=keyboard, payload=payload)


"""Подключение бота"""
VK_API_VERSION = '5.120'
GROUP_ID = 197300375
VK_API_ACCESS_TOKEN = '50b21743f85bf752ccb5a0f29a1009e0f7bac25bbd6e0ef9211acb4fdb33bb1d5f11099497f14409c561c'
vk_session = vk_api.VkApi(token=VK_API_ACCESS_TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, 197300375)

"""Все наши переменные"""
film_or_serial = 0
films_list = []
temp = 0
min_rating = 6
max_rating = 10
min_year = 2000
max_year = 2020
genre_id = 'Не выбран'
second_genre_id = 'Не выбран'
kind_of_sorting = 'По кол-ву голосов imdb'
user_settings = {}


def our_keyboard():
    """Главное меню - начало диалога или любое сообщение """

    if payload is None or payload == 0:
        keyboard = VkKeyboard(one_time=False)
        # keyboard.add_button('Я уже знаю что посмотреть', payload=1, color=VkKeyboardColor.PRIMARY)
        # keyboard.add_line()
        keyboard.add_button('Я хочу выбрать рандомно', VkKeyboardColor.PRIMARY, payload='2')
        keyboard.add_line()
        keyboard.add_button('Продвинутый поиск', VkKeyboardColor.PRIMARY, payload='3')
        keyboard.add_line()
        keyboard.add_button('Топ 100 фильмов или сериалов', VkKeyboardColor.PRIMARY, payload='100')
        return keyboard.get_keyboard()

    elif payload == 2:
        """Главное меню - рандомный поиск """

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Фильм', VkKeyboardColor.PRIMARY, payload='5')
        keyboard.add_button('Сериал', VkKeyboardColor.PRIMARY, payload='6')
        keyboard.add_line()
        keyboard.add_button('Завершенный сериал', VkKeyboardColor.PRIMARY, payload='300')
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload='0')
        return keyboard.get_keyboard()

    elif payload in [5, 6, 300]:
        """Цифры для выбора в рандоме"""

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('1', VkKeyboardColor.PRIMARY, payload='7')
        keyboard.add_button('2', VkKeyboardColor.PRIMARY, payload='8')
        keyboard.add_button('3', VkKeyboardColor.PRIMARY, payload='9')
        keyboard.add_button('4', VkKeyboardColor.PRIMARY, payload='10')
        keyboard.add_line()
        keyboard.add_button('5', VkKeyboardColor.PRIMARY, payload='11')
        keyboard.add_button('6', VkKeyboardColor.PRIMARY, payload='12')
        keyboard.add_button('7', VkKeyboardColor.PRIMARY, payload='13')
        keyboard.add_button('8', VkKeyboardColor.PRIMARY, payload='14')
        keyboard.add_line()
        keyboard.add_button('9', VkKeyboardColor.PRIMARY, payload='15')
        keyboard.add_button('10', VkKeyboardColor.PRIMARY, payload='16')
        keyboard.add_button('11', VkKeyboardColor.PRIMARY, payload='17')
        keyboard.add_button('12', VkKeyboardColor.PRIMARY, payload='18')
        if payload == 5 or film_or_serial == 5:
            keyboard.add_line()
            keyboard.add_button('Переключить на сериалы', VkKeyboardColor.DEFAULT, payload='6')
            keyboard.add_line()
            keyboard.add_button('Переключить на завершенные сериалы', VkKeyboardColor.DEFAULT, payload='300')
            keyboard.add_line()
            keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload='0')
            return keyboard.get_keyboard()
        elif payload == 6 or film_or_serial == 6:
            keyboard.add_line()
            keyboard.add_button('Переключить на фильмы', VkKeyboardColor.DEFAULT, payload='5')
            keyboard.add_line()
            keyboard.add_button('Переключить на завершенные сериалы', VkKeyboardColor.DEFAULT, payload='300')
            keyboard.add_line()
            keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload='0')
            return keyboard.get_keyboard()
        elif payload == 300 or film_or_serial == 300:
            keyboard.add_line()
            keyboard.add_button('Переключить на фильмы', VkKeyboardColor.DEFAULT, payload='5')
            keyboard.add_line()
            keyboard.add_button('Переключить на сериалы', VkKeyboardColor.DEFAULT, payload='6')
            keyboard.add_line()
            keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload='0')
            return keyboard.get_keyboard()
        else:
            keyboard.add_line()
            keyboard.add_button('Назад в меню поиска', VkKeyboardColor.PRIMARY, payload='3')
            keyboard.add_line()
            keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload='0')
            return keyboard.get_keyboard()

    elif payload in [100, 61, 65]:
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Топ 100 фильмов', VkKeyboardColor.PRIMARY, payload='61')
        keyboard.add_line()
        keyboard.add_button('Топ 100 сериалов', VkKeyboardColor.PRIMARY, payload='65')
        keyboard.add_line()
        keyboard.add_button('Топ 100 фильмов по одному жанру', VkKeyboardColor.PRIMARY, payload='64')
        keyboard.add_line()
        keyboard.add_button('Топ 100 сериалов по одному жанру', VkKeyboardColor.PRIMARY, payload='62')
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload='0')
        return keyboard.get_keyboard()

    elif payload == 62:
        """Выбор жанра для топ 100 сериалов"""

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('1', VkKeyboardColor.PRIMARY, payload='301')
        keyboard.add_button('2', VkKeyboardColor.PRIMARY, payload='302')
        keyboard.add_button('3', VkKeyboardColor.PRIMARY, payload='303')
        keyboard.add_button('4', VkKeyboardColor.PRIMARY, payload='304')
        keyboard.add_line()
        keyboard.add_button('5', VkKeyboardColor.PRIMARY, payload='305')
        keyboard.add_button('6', VkKeyboardColor.PRIMARY, payload='306')
        keyboard.add_button('7', VkKeyboardColor.PRIMARY, payload='307')
        keyboard.add_button('8', VkKeyboardColor.PRIMARY, payload='308')
        keyboard.add_line()
        keyboard.add_button('9', VkKeyboardColor.PRIMARY, payload='309')
        keyboard.add_button('10', VkKeyboardColor.PRIMARY, payload='310')
        keyboard.add_button('11', VkKeyboardColor.PRIMARY, payload='311')
        keyboard.add_button('12', VkKeyboardColor.PRIMARY, payload='312')
        keyboard.add_line()
        keyboard.add_button('В меню топов', VkKeyboardColor.DEFAULT, payload='100')
        keyboard.add_line()
        keyboard.add_button('В главное меню', VkKeyboardColor.DEFAULT, payload='0')
        return keyboard.get_keyboard()

    elif payload == 64:
        """Выбор жанра для топ 100 фильмов"""

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('1', VkKeyboardColor.PRIMARY, payload='313')
        keyboard.add_button('2', VkKeyboardColor.PRIMARY, payload='314')
        keyboard.add_button('3', VkKeyboardColor.PRIMARY, payload='315')
        keyboard.add_button('4', VkKeyboardColor.PRIMARY, payload='316')
        keyboard.add_line()
        keyboard.add_button('5', VkKeyboardColor.PRIMARY, payload='317')
        keyboard.add_button('6', VkKeyboardColor.PRIMARY, payload='319')
        keyboard.add_button('7', VkKeyboardColor.PRIMARY, payload='319')
        keyboard.add_button('8', VkKeyboardColor.PRIMARY, payload='320')
        keyboard.add_line()
        keyboard.add_button('9', VkKeyboardColor.PRIMARY, payload='321')
        keyboard.add_button('10', VkKeyboardColor.PRIMARY, payload='322')
        keyboard.add_button('11', VkKeyboardColor.PRIMARY, payload='323')
        keyboard.add_button('12', VkKeyboardColor.PRIMARY, payload='324')
        keyboard.add_line()
        keyboard.add_button('В меню топов', VkKeyboardColor.DEFAULT, payload='100')
        keyboard.add_line()
        keyboard.add_button('В главное меню', VkKeyboardColor.DEFAULT, payload='0')
        return keyboard.get_keyboard()

    elif payload == 3:
        """Главное меню - продвинутый поиск"""

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Выбрать год', VkKeyboardColor.PRIMARY, payload='19')
        keyboard.add_button('Выбрать рейтинг', VkKeyboardColor.PRIMARY, payload='20')
        keyboard.add_line()
        keyboard.add_button('Выбрать жанр', VkKeyboardColor.PRIMARY, payload='21')
        keyboard.add_button('Второй жанр', VkKeyboardColor.PRIMARY, payload='56')
        keyboard.add_line()
        keyboard.add_button('Выбрать сортировку', VkKeyboardColor.PRIMARY, payload='54')
        keyboard.add_line()
        keyboard.add_button('Показать выбранные', VkKeyboardColor.PRIMARY, payload='543')
        keyboard.add_line()
        keyboard.add_button('Выбранные настройки', VkKeyboardColor.DEFAULT, payload='55')
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload='0')
        return keyboard.get_keyboard()

    elif payload == 19:
        """Продвинутый поиск - изменение года """

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Начальный год', VkKeyboardColor.PRIMARY, payload='23')
        keyboard.add_button('Конечный год', VkKeyboardColor.PRIMARY, payload='24')
        keyboard.add_line()
        keyboard.add_button('В меню поиска', VkKeyboardColor.PRIMARY, payload='3')
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload='0')
        return keyboard.get_keyboard()

    elif payload == 23 or payload == 24:
        """Выбор года для начального и конечного года"""

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('1989', VkKeyboardColor.PRIMARY, payload='201')
        keyboard.add_button('1990', VkKeyboardColor.PRIMARY, payload='202')
        keyboard.add_button('1991', VkKeyboardColor.PRIMARY, payload='203')
        keyboard.add_button('1992', VkKeyboardColor.PRIMARY, payload='204')
        keyboard.add_line()
        keyboard.add_button('1993', VkKeyboardColor.PRIMARY, payload='205')
        keyboard.add_button('1994', VkKeyboardColor.PRIMARY, payload='206')
        keyboard.add_button('1995', VkKeyboardColor.PRIMARY, payload='207')
        keyboard.add_button('1996', VkKeyboardColor.PRIMARY, payload='208')
        keyboard.add_line()
        keyboard.add_button('1997', VkKeyboardColor.PRIMARY, payload='209')
        keyboard.add_button('1998', VkKeyboardColor.PRIMARY, payload='210')
        keyboard.add_button('1999', VkKeyboardColor.PRIMARY, payload='211')
        keyboard.add_button('2000', VkKeyboardColor.PRIMARY, payload='212')
        keyboard.add_line()
        keyboard.add_button('2001', VkKeyboardColor.PRIMARY, payload='213')
        keyboard.add_button('2002', VkKeyboardColor.PRIMARY, payload='214')
        keyboard.add_button('2003', VkKeyboardColor.PRIMARY, payload='215')
        keyboard.add_button('2004', VkKeyboardColor.PRIMARY, payload='216')
        keyboard.add_line()
        keyboard.add_button('Следующая страница', VkKeyboardColor.PRIMARY, payload='99')
        if payload == 23:
            keyboard.add_line()
            keyboard.add_button('Переключить на конечный год', VkKeyboardColor.DEFAULT, payload='24')
            keyboard.add_line()
        elif payload == 24:
            keyboard.add_line()
            keyboard.add_button('Переключить на начальный год', VkKeyboardColor.DEFAULT, payload='23')
            keyboard.add_line()
        keyboard.add_button('В меню поиска', VkKeyboardColor.DEFAULT, payload='3')
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload='0')
        return keyboard.get_keyboard()

    elif payload == 99:
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('2005', VkKeyboardColor.PRIMARY, payload='217')
        keyboard.add_button('2006', VkKeyboardColor.PRIMARY, payload='218')
        keyboard.add_button('2007', VkKeyboardColor.PRIMARY, payload='219')
        keyboard.add_button('2008', VkKeyboardColor.PRIMARY, payload='220')
        keyboard.add_line()
        keyboard.add_button('2009', VkKeyboardColor.PRIMARY, payload='221')
        keyboard.add_button('2010', VkKeyboardColor.PRIMARY, payload='222')
        keyboard.add_button('2011', VkKeyboardColor.PRIMARY, payload='223')
        keyboard.add_button('2012', VkKeyboardColor.PRIMARY, payload='224')
        keyboard.add_line()
        keyboard.add_button('2013', VkKeyboardColor.PRIMARY, payload='225')
        keyboard.add_button('2014', VkKeyboardColor.PRIMARY, payload='226')
        keyboard.add_button('2015', VkKeyboardColor.PRIMARY, payload='227')
        keyboard.add_button('2016', VkKeyboardColor.PRIMARY, payload='228')
        keyboard.add_line()
        keyboard.add_button('2017', VkKeyboardColor.PRIMARY, payload='229')
        keyboard.add_button('2018', VkKeyboardColor.PRIMARY, payload='230')
        keyboard.add_button('2019', VkKeyboardColor.PRIMARY, payload='231')
        keyboard.add_button('2020', VkKeyboardColor.PRIMARY, payload='232')
        keyboard.add_line()
        keyboard.add_button('Предыдущая страница', VkKeyboardColor.PRIMARY, payload='23')
        if user_settings[user_id]['year_choose'] == 'start':
            keyboard.add_line()
            keyboard.add_button('Переключить на конечный год', VkKeyboardColor.DEFAULT, payload='24')
            keyboard.add_line()
        elif user_settings[user_id]['year_choose'] == 'end':
            keyboard.add_line()
            keyboard.add_button('Переключить на начальный год', VkKeyboardColor.DEFAULT, payload='23')
            keyboard.add_line()
        keyboard.add_button('В меню поиска', VkKeyboardColor.DEFAULT, payload='3')
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload='0')
        return keyboard.get_keyboard()

    elif payload == 20:
        """Продвинутый поиск - изменение рейтинга """

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Мин. рейтинг', VkKeyboardColor.PRIMARY, payload='25')
        keyboard.add_button('Макс. рейтинг', VkKeyboardColor.PRIMARY, payload='26')
        keyboard.add_line()
        keyboard.add_button('В меню поиска', VkKeyboardColor.PRIMARY, payload='3')
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload='0')
        return keyboard.get_keyboard()

    elif payload in [25, 26]:
        """Продвинутый поиск - меню для изменение рейтинга """

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('1', VkKeyboardColor.PRIMARY, payload='39')
        keyboard.add_button('2', VkKeyboardColor.PRIMARY, payload='40')
        keyboard.add_button('3', VkKeyboardColor.PRIMARY, payload='41')
        keyboard.add_button('4', VkKeyboardColor.PRIMARY, payload='42')
        keyboard.add_line()
        keyboard.add_button('5', VkKeyboardColor.PRIMARY, payload='43')
        keyboard.add_button('6', VkKeyboardColor.PRIMARY, payload='44')
        keyboard.add_button('7', VkKeyboardColor.PRIMARY, payload='45')
        keyboard.add_button('8', VkKeyboardColor.PRIMARY, payload='46')
        keyboard.add_line()
        keyboard.add_button('9', VkKeyboardColor.PRIMARY, payload='47')
        keyboard.add_button('10', VkKeyboardColor.PRIMARY, payload='48')
        if temp == 'min' or payload == 25:
            keyboard.add_line()
            keyboard.add_button('Переключить на макс. рейтинг', VkKeyboardColor.DEFAULT, payload='26')
            keyboard.add_line()
        elif temp == 'max' or payload == 26:
            keyboard.add_line()
            keyboard.add_button('Переключить на мин. рейтинг', VkKeyboardColor.DEFAULT, payload='25')
            keyboard.add_line()
        keyboard.add_button('В меню поиска', VkKeyboardColor.DEFAULT, payload='3')
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload='0')
        return keyboard.get_keyboard()

    elif payload == 21:
        """Продвинутый поиск - изменение жанра """

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('1', VkKeyboardColor.PRIMARY, payload='27')
        keyboard.add_button('2', VkKeyboardColor.PRIMARY, payload='28')
        keyboard.add_button('3', VkKeyboardColor.PRIMARY, payload='29')
        keyboard.add_button('4', VkKeyboardColor.PRIMARY, payload='30')
        keyboard.add_line()
        keyboard.add_button('5', VkKeyboardColor.PRIMARY, payload='31')
        keyboard.add_button('6', VkKeyboardColor.PRIMARY, payload='32')
        keyboard.add_button('7', VkKeyboardColor.PRIMARY, payload='33')
        keyboard.add_button('8', VkKeyboardColor.PRIMARY, payload='34')
        keyboard.add_line()
        keyboard.add_button('9', VkKeyboardColor.PRIMARY, payload='35')
        keyboard.add_button('10', VkKeyboardColor.PRIMARY, payload='36')
        keyboard.add_button('11', VkKeyboardColor.PRIMARY, payload='37')
        keyboard.add_button('12', VkKeyboardColor.PRIMARY, payload='38')
        keyboard.add_line()
        keyboard.add_button('Выбрать второй жанр', VkKeyboardColor.DEFAULT, payload='56')
        keyboard.add_line()
        keyboard.add_button('В меню поиска', VkKeyboardColor.DEFAULT, payload='3')
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload='0')
        return keyboard.get_keyboard()

    elif payload == 56:
        """Продвинутый поиск - изменение жанра """

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('1', VkKeyboardColor.PRIMARY, payload='27')
        keyboard.add_button('2', VkKeyboardColor.PRIMARY, payload='28')
        keyboard.add_button('3', VkKeyboardColor.PRIMARY, payload='29')
        keyboard.add_button('4', VkKeyboardColor.PRIMARY, payload='30')
        keyboard.add_line()
        keyboard.add_button('5', VkKeyboardColor.PRIMARY, payload='31')
        keyboard.add_button('6', VkKeyboardColor.PRIMARY, payload='32')
        keyboard.add_button('7', VkKeyboardColor.PRIMARY, payload='33')
        keyboard.add_button('8', VkKeyboardColor.PRIMARY, payload='34')
        keyboard.add_line()
        keyboard.add_button('9', VkKeyboardColor.PRIMARY, payload='35')
        keyboard.add_button('10', VkKeyboardColor.PRIMARY, payload='36')
        keyboard.add_button('11', VkKeyboardColor.PRIMARY, payload='37')
        keyboard.add_button('12', VkKeyboardColor.PRIMARY, payload='38')
        keyboard.add_line()
        keyboard.add_button('Выбрать первый жанр', VkKeyboardColor.DEFAULT, payload='21')
        keyboard.add_line()
        keyboard.add_button('В меню поиска', VkKeyboardColor.DEFAULT, payload='3')
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload='0')
        return keyboard.get_keyboard()

    elif payload == 54:
        """Продвинутый поиск - выбор сортировки"""
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('По году', color=VkKeyboardColor.PRIMARY, payload='70')
        keyboard.add_button('По рейтингу', VkKeyboardColor.PRIMARY, payload='71')
        keyboard.add_line()
        keyboard.add_button('По году и рейтингу', VkKeyboardColor.PRIMARY, payload='72')
        keyboard.add_line()
        keyboard.add_button('По кол-ву голосов imdb', VkKeyboardColor.PRIMARY, payload='73')
        keyboard.add_line()
        keyboard.add_button('В меню поиска', VkKeyboardColor.DEFAULT, payload='3')
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload='0')
        return keyboard.get_keyboard()

    elif payload == 543:
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('1', VkKeyboardColor.PRIMARY, payload='601')
        keyboard.add_button('5', VkKeyboardColor.PRIMARY, payload='602')
        keyboard.add_button('10', VkKeyboardColor.PRIMARY, payload='603')
        keyboard.add_button('25', VkKeyboardColor.PRIMARY, payload='604')
        keyboard.add_line()
        keyboard.add_button('В меню поиска', VkKeyboardColor.DEFAULT, payload='3')
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload='0')
        return keyboard.get_keyboard()


class SetSettings():
    def __init__(self, user_id_class_f):
        self.start_year = 2000
        self.end_year = 2020
        self.min_rating = 6
        self.max_rating = 10
        self.first_genre = None
        self.second_genre = None
        self.sorting = 4
        self.film_or_serial = 0

    def set_settings(self, user_id_class, st_year, en_year, mn_rating, mx_rating, fs_genre, sc_genre, sort, users_s,
                     film_or_ser):
        self.start_year = st_year,
        self.end_year = en_year,
        self.min_rating = mn_rating,
        self.max_rating = mx_rating,
        self.first_genre = fs_genre,
        self.second_genre = sc_genre,
        self.sorting = sort,
        self.film_or_serial = film_or_ser
        users_s[user_id_class] = {
            'start_year': self.start_year[0],
            'end_year': self.end_year[0],
            'min_rating': self.min_rating[0],
            'max_rating': self.max_rating[0],
            'first_genre': self.first_genre[0],
            'second_genre': self.second_genre[0],
            'sorting': self.sorting,
            'film_or_ser': self.film_or_serial
        }


while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                peer_id_in = event.obj['message']['peer_id']
                user_id = event.obj['message']['from_id']
                user_get = vk.users.get(user_ids=(user_id))
                user_get = user_get[0]
                first_name = user_get['first_name']
                last_name = user_get['last_name']
                full_name = first_name + " " + last_name
                print('Сообщение пришло в: ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
                print(f"Отправитель - {full_name}")
                print(f"Новое сообщение: {event.obj['message']['text']}")
                print('_' * 30)

                if user_settings.get(user_id) is None:
                    user = SetSettings(user_id)
                    user.set_settings(user_id, min_year, max_year, min_rating, max_rating, genre_id,
                                      second_genre_id, kind_of_sorting, user_settings, film_or_serial)

                try:
                    if event.obj['message']['payload'] is not None:
                        payload = int(event.obj['message']['payload'])
                    else:
                        payload = None

                except Exception as error1:
                    print(error1)
                    payload = None

                keyboard = our_keyboard()

                if payload is None:
                    send_message(peer_id=peer_id_in, message='Мы в главном меню', keyboard=keyboard)

                # Рандомный поиск
                elif payload == 2:
                    send_message(peer_id=peer_id_in, message='Для рандомного выбора нужно выбрать категорию:',
                                 keyboard=keyboard)

                # Выбор жанра для рандомного поиска
                elif payload in [5, 6, 300]:
                    send_message(peer_id=peer_id_in, message='Теперь нужно выбрать жанр:\n'
                                                             f'{category_list}',
                                 keyboard=keyboard)
                    user_settings[user_id]['film_or_ser'] = payload

                # Если переключаем категории в рандомном поиске
                if payload in [5, 6, 300]:
                    keyboard_for_change = our_keyboard()
                    if payload == 5:
                        named = 'фильмы'
                    elif payload == 6:
                        named = 'сериалы'
                    elif payload == 300:
                        named = 'завершенные сериалы'
                    send_message(peer_id=peer_id_in, message=f'Категория успешно изменена на "{named}"',
                                 keyboard=keyboard_for_change)
                    user_settings[user_id]['film_or_ser'] = payload

                # Если ответ на выбор жанра правильный и есть в списке. Показываем рандомные фильмы / сериалы
                if payload in [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]:
                    genre_id_for_random = payload - 6
                    # Подбор рандомного фильма
                    if user_settings[user_id]['film_or_ser'] == 5:
                        db = get_connection()
                        cursor = db.cursor()
                        selector = ('SELECT * FROM movie INNER JOIN genre_movie ON movie.id = genre_movie.movie_id '
                                    'WHERE genre_id = %s and rating > 7 and premier > 1998 and type_id = 0 '
                                    'and duration != 0 '
                                    'and votes > 25000 ORDER BY RAND() LIMIT 1')
                        cursor.execute(selector, (genre_id_for_random,))
                        checker = cursor.fetchall()
                        prod_actor_genre = actors_producers_genres(checker[0][0])
                        our_film = f"---Фильм---\n▶{checker[0][1]}\n\n✓Жанры - {prod_actor_genre[2]}" \
                                   f"\n✓Год премьеры - {checker[0][3]}\n✓Рейтинг - " \
                                   f"{checker[0][5]}\n✓Продолжительность - {checker[0][6]} мин\n" \
                                   f"✓Количество голосов imdb - {checker[0][7]}\n\n" \
                                   f"🎬Продюсер - {prod_actor_genre[0]}\n✪Актеры - {prod_actor_genre[1]}\n\n" \
                                   f"Ссылка  - {checker[0][8]}"

                        send_message(peer_id=peer_id_in, message='А вот и твой фильм:\n'
                                                                 f'{our_film}',
                                     keyboard=keyboard)

                    # Подбор рандомного сериала
                    elif user_settings[user_id]['film_or_ser'] == 6:
                        db = get_connection()
                        cursor = db.cursor()
                        selector = ('SELECT * FROM movie INNER JOIN genre_movie ON movie.id = genre_movie.movie_id '
                                    'WHERE genre_id = %s and rating > 7 and premier > 1998 and type_id = 1 '
                                    'and duration != 0 '
                                    'and votes > 25000 ORDER BY RAND() LIMIT 1')
                        cursor.execute(selector, (genre_id_for_random,))
                        checker = cursor.fetchall()
                        prod_actor_genre = actors_producers_genres(checker[0][0])
                        our_film = f"---Сериал---\n▶{checker[0][1]}\n\n✓Жанры - {prod_actor_genre[2]}" \
                                   f"\n✓Год премьеры - {checker[0][3]}\n✓Рейтинг - " \
                                   f"{checker[0][5]}\n✓Продолжительность - {checker[0][6]} мин\n" \
                                   f"✓Количество голосов imdb - {checker[0][7]}\n\n" \
                                   f"🎬Продюсер - {prod_actor_genre[0]}\n✪Актеры - {prod_actor_genre[1]}\n\n" \
                                   f"Ссылка  - {checker[0][8]}"

                        send_message(peer_id=peer_id_in, message='А вот и твой сериал:\n'
                                                                 f'{our_film}',
                                     keyboard=keyboard)

                    elif user_settings[user_id]['film_or_ser'] == 300:
                        db = get_connection()
                        cursor = db.cursor()
                        selector = ('SELECT * FROM movie INNER JOIN genre_movie ON movie.id = genre_movie.movie_id '
                                    'WHERE genre_id = %s and rating > 7 and premier > 1998 and type_id = 2 '
                                    'and duration != 0 '
                                    'and votes > 25000 ORDER BY RAND() LIMIT 1')
                        cursor.execute(selector, (genre_id_for_random,))
                        checker = cursor.fetchall()
                        prod_actor_genre = actors_producers_genres(checker[0][0])
                        our_film = f"---Сериал---\n▶{checker[0][1]}\n\n✓Жанры - {prod_actor_genre[2]}" \
                                   f"\n✓Год премьеры - {checker[0][3]}\n✓Последней сезон - {checker[0][4]}" \
                                   f"\n✓Рейтинг - " \
                                   f"{checker[0][5]}\n✓Продолжительность - {checker[0][6]} мин\n" \
                                   f"✓Количество голосов imdb - {checker[0][7]}\n\n" \
                                   f"🎬Продюсер - {prod_actor_genre[0]}\n✪Актеры - {prod_actor_genre[1]}\n\n" \
                                   f"Ссылка  - {checker[0][8]}"

                        send_message(peer_id=peer_id_in, message='А вот и твой завершенный сериал:\n'
                                                                 f'{our_film}',
                                     keyboard=keyboard)

                # Все для топ 100
                if payload == 100:
                    send_message(peer_id=peer_id_in, message='Меню топов',
                                 keyboard=keyboard)

                elif payload in [61, 62, 64, 65]:
                    if payload == 61:
                        selector_for_100_films = 'SELECT * FROM top_250_movie'
                        db_100 = get_connection()
                        cursor_100 = db_100.cursor()
                        cursor_100.execute(selector_for_100_films)
                        to_250 = cursor_100.fetchall()
                        to_250 = to_250[:100]
                        to_250.reverse()
                        answer = ''
                        count = len(to_250)
                        for film in to_250:
                            answer += f"{count}-----{film[1]}-----\n"
                            answer += f'✓Жанры: {film[2]}\n'
                            answer += f'✓Рейтинг: {film[3]}\n'
                            answer += f'✓Год: {film[4]}\n'
                            answer += f'✓Количество голосов: {film[-1]}\n\n'
                            count -= 1
                            if count % 25 == 0:
                                send_message(peer_id=peer_id_in, message=f'{answer}',
                                             keyboard=keyboard)
                                answer = ''

                    elif payload == 62:
                        send_message(peer_id=peer_id_in, message='Теперь нужно выбрать жанр для нашего топа:\n'
                                                                 f'{category_list}',
                                     keyboard=keyboard)

                    elif payload == 64:
                        send_message(peer_id=peer_id_in, message='Теперь нужно выбрать жанр для нашего топа:\n'
                                                                 f'{category_list}',
                                     keyboard=keyboard)

                    elif payload == 65:
                        selector_for_100_serials = 'SELECT * FROM top_250_serials'
                        db_1005 = get_connection()
                        cursor_1005 = db_1005.cursor()
                        cursor_1005.execute(selector_for_100_serials)
                        top_films_250 = cursor_1005.fetchall()
                        top_films_250 = top_films_250[:100]
                        top_films_250.reverse()
                        answer2 = ''
                        count1 = len(top_films_250)
                        for film in top_films_250:
                            answer2 += f"{count1}-----{film[1]}-----\n"
                            answer2 += f'✓Жанры: {film[2]}\n'
                            answer2 += f'✓Рейтинг: {film[3]}\n'
                            answer2 += f'✓Год: {film[4]}\n'
                            answer2 += f'✓Количество голосов: {film[-1]}\n\n'
                            count1 -= 1
                            if count1 % 25 == 0:
                                send_message(peer_id=peer_id_in, message=f'{answer2}',
                                             keyboard=keyboard)
                                answer2 = ''

                # Жанр для топ 100 сериалов
                if payload in [301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312]:
                    genre_for_top_100 = payload - 300
                    serial_counter1 = 1
                    db_top_ser = get_connection()
                    cursor_top_ser = db_top_ser.cursor()
                    selector = ('SELECT * FROM movie INNER JOIN genre_movie ON movie.id = genre_movie.movie_id '
                                'WHERE genre_id = %s and rating > 5 and premier > 1995 and duration != 0 and '
                                'votes > 20000 and type_id != 0')

                    cursor_top_ser.execute(selector, (genre_for_top_100,))
                    mass_serial = cursor_top_ser.fetchall()
                    mass_serial.sort(key=lambda x: (x[7], x[5], x[3]), reverse=True)
                    mass_serial = mass_serial[:100]
                    mass_serial.reverse()
                    top_serials = ''
                    ser_counter = len(mass_serial)
                    for film in mass_serial:
                        top_serials += f"{ser_counter}-----{film[1]}-----\n"
                        top_serials += f'✓Рейтинг: {film[5]}\n'
                        top_serials += f'✓Год: {film[3]}\n'
                        top_serials += f'✓Количество голосов: {film[7]}\n\n'
                        ser_counter -= 1
                        serial_counter1 += 1
                        if ser_counter % 25 == 0:
                            print(top_serials)
                            send_message(peer_id=peer_id_in, message=f'{top_serials}',
                                         keyboard=keyboard)
                            top_serials = ''

                # Жанр для топ 100 фильмов
                elif payload in [313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324]:
                    genre_for_top_100 = payload - 312
                    fil_counter1 = 1
                    db_top_film = get_connection()
                    cursor_top_film = db_top_film.cursor()
                    selector = ('SELECT * FROM movie INNER JOIN genre_movie ON movie.id = genre_movie.movie_id '
                                'WHERE genre_id = %s and rating > 5 and premier > 1995 and duration != 0 and '
                                'votes > 20000 and type_id = 0')

                    cursor_top_film.execute(selector, (genre_for_top_100,))
                    mass_films = cursor_top_film.fetchall()
                    mass_films.sort(key=lambda x: (x[7], x[5], x[3]), reverse=True)
                    mass_films = mass_films[:100]
                    mass_films.reverse()

                    top_films = ''
                    fil_counter = 100
                    for film in mass_films:
                        top_films += f"{fil_counter}-----{film[1]}-----\n"
                        top_films += f'✓Рейтинг: {film[5]}\n'
                        top_films += f'✓Год: {film[3]}\n'
                        top_films += f'✓Количество голосов: {film[7]}\n\n'
                        fil_counter -= 1
                        fil_counter1 += 1
                        if fil_counter % 25 == 0:
                            send_message(peer_id=peer_id_in, message=f'{top_films}',
                                         keyboard=keyboard)
                            top_films = ''

                # Продвинутый поиск
                if payload == 3:
                    send_message(peer_id=peer_id_in, message='В меню продвинутого поиска: ',
                                 keyboard=keyboard)

                # Меню изменения года
                elif payload == 19:
                    send_message(peer_id=peer_id_in, message='Меню изменения года',
                                 keyboard=keyboard)

                # заносим в переменную год начала
                elif payload == 23:
                    user_settings[user_id]['year_choose'] = 'start'
                    send_message(peer_id=peer_id_in, message='Выбираем минимальный год: ',
                                 keyboard=keyboard)

                # заносим в переменную год конца
                elif payload == 24:
                    user_settings[user_id]['year_choose'] = 'end'
                    send_message(peer_id=peer_id_in, message='Выбираем максимальный год: ',
                                 keyboard=keyboard)

                # Проверяем нажатый год
                elif payload in [201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217,
                               218, 219,
                               220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232]:

                    if user_settings[user_id]['year_choose'] == 'start':
                        if payload + 1788 >= user_settings[user_id]["end_year"]:
                            send_message(peer_id=peer_id_in, message=f'Минимальный год не может быть больше '
                                                                     f'или равным максимальному году, попробуйте '
                                                                     f'выбрать год еще раз\n'
                                                                     f'Год, который выбран как максимальный '
                                                                     f'-{user_settings[user_id]["end_year"]}',
                                         keyboard=keyboard)
                        else:
                            user_settings[user_id]["start_year"] = payload + 1788
                            print(user_settings[user_id]["start_year"])
                            send_message(peer_id=peer_id_in, message=f'Минимальный год успешно выбран -'
                                                                     f' {user_settings[user_id]["start_year"]}\n\n'
                                                                     f'Чтобы изменить его еще раз, просто нажмите '
                                                                     f'на нужный год в этом же меню.\n '
                                                                     f'Чтобы перейти к выбору "Конечного года" - '
                                                                     f'нажмите на кнопку "Переключить на конечный '
                                                                     f'год\n\nЧтобы вернуться к остальным фильтрам '
                                                                     f'- нажмите "В меню поиска"')

                    elif user_settings[user_id]['year_choose'] == 'end':
                        if payload + 1788 <= user_settings[user_id]["start_year"]:
                            send_message(peer_id=peer_id_in, message=f'Максимальный год не может быть меньше '
                                                                     f'или равным минимальному году. Попробуйте выбрать'
                                                                     f' год еще раз\n'
                                                                     f'Год, который выбран как минимальный '
                                                                     f'-{user_settings[user_id]["start_year"]}',
                                         keyboard=keyboard)
                        else:
                            user_settings[user_id]["end_year"] = payload + 1788
                            send_message(peer_id=peer_id_in, message=f'Максимальный год успешно выбран - '
                                                                     f'{user_settings[user_id]["end_year"]}.\n\n'
                                                                     f'Чтобы изменить его еще раз, просто нажмите '
                                                                     f'на нужный год в этом же меню.\n'
                                                                     f'Чтобы перейти к выбору "Начального года" - '
                                                                     f'нажмите на кнопку "Переключить на начальный '
                                                                     f'год\n\nЧтобы вернуться к остальным фильтрам '
                                                                     f'- нажмите "В меню поиска"')

                # Переключение страниц
                elif payload == 99:
                    send_message(peer_id=peer_id_in, message='Открываем следующую страницу: ',
                                 keyboard=keyboard)

                # Меню изменения рейтинга
                if payload == 20:
                    send_message(peer_id=peer_id_in, message='Меню изменения рейтинга',
                                 keyboard=keyboard)

                # Выбираем минимальный или максимальный рейтинг и заносим в базу
                elif payload in [25, 26]:
                    if payload == 25:
                        user_settings[user_id]['rating_choose'] = 'min'
                        send_message(peer_id=peer_id_in, message='В меню изменения начального рейтинга',
                                     keyboard=keyboard)
                    elif payload == 26:
                        user_settings[user_id]['rating_choose'] = 'max'
                        send_message(peer_id=peer_id_in, message='В меню изменения конечного рейтинга',
                                     keyboard=keyboard)

                # Изменяем максимальный или минимальный рейтинг
                if payload in [39, 40, 41, 42, 43, 44, 45, 46, 47, 48]:
                    if user_settings[user_id]['rating_choose'] == 'min':
                        if payload - 38 >= user_settings[user_id]["max_rating"]:
                            send_message(peer_id=peer_id_in,
                                         message=f'Минимальный рейтинг нельзя выставить больше или равным '
                                                 f'максимальному. Ваш максимальный рейтинг - '
                                                 f'{user_settings[user_id]["max_rating"]}',
                                         keyboard=keyboard)
                        else:
                            user_settings[user_id]["min_rating"] = payload - 38
                            send_message(peer_id=peer_id_in,
                                         message=f'Минимальный рейтинг успешно изменен на '
                                                 f'{user_settings[user_id]["min_rating"]}\n'
                                                 f'Можно вернуться в "меню поиска" чтобы настроить '
                                                 f'остальные фильтры или выбрать '
                                                 f'рейтинг еще раз из этого меню, просто нажав на цифру',
                                         keyboard=keyboard)

                    elif user_settings[user_id]['rating_choose'] == 'max':
                        if payload - 38 <= user_settings[user_id]["min_rating"]:
                            send_message(peer_id=peer_id_in,
                                         message=f'Максимальный рейтинг нельзя выставить меньше или равным '
                                                 f'минимальному. Ваш минимальный рейтинг - '
                                                 f'{user_settings[user_id]["min_rating"]}',
                                         keyboard=keyboard)
                        else:
                            user_settings[user_id]["max_rating"] = payload - 38
                            send_message(peer_id=peer_id_in,
                                         message=f'Максимальный рейтинг успешно изменен на '
                                                 f'{user_settings[user_id]["max_rating"]}\n'
                                                 f'Можно вернуться в "меню поиска" чтобы настроить '
                                                 f'остальные фильтры или выбрать '
                                                 f'рейтинг еще раз из этого меню, просто нажав на цифру',
                                         keyboard=keyboard)

                # Меню изменение жанра
                if payload == 21:
                    user_settings[user_id]['choose_genre'] = 'first'
                    send_message(peer_id=peer_id_in, message='Теперь нужно выбрать первый жанр:\n'
                                                             f'{category_list}',
                                 keyboard=keyboard)
                elif payload == 56:
                    user_settings[user_id]['choose_genre'] = 'second'
                    send_message(peer_id=peer_id_in, message='Теперь нужно выбрать жанр:\n'
                                                             f'{category_list}',
                                 keyboard=keyboard)

                # Изменение первого и второго жанра
                elif payload in [27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38]:
                    if user_settings[user_id]['choose_genre'] == 'first':
                        user_settings[user_id]["first_genre"] = list_of_genres[payload - 26]["Genre name"]
                        send_message(peer_id=peer_id_in,
                                     message=f'Первый жанр был успешно выбран - '
                                             f'{user_settings[user_id]["first_genre"]}.\n\n'
                                             'При выборе жанра можно несколько раз нажимать на указанные'
                                             ' кнопки с цифрами, если Вы решили изменить свое решение. '
                                             'Если же жанр выбран'
                                             ' правильно - можно вернуться к настройкам остальных фильтров нажам на '
                                             '"В меню поиска"',
                                     keyboard=keyboard)

                    elif user_settings[user_id]['choose_genre'] == 'second':
                        user_settings[user_id]["second_genre"] = list_of_genres[payload - 26]["Genre name"]
                        send_message(peer_id=peer_id_in,
                                     message=f'Второй жанр был успешно выбран - '
                                             f'{user_settings[user_id]["second_genre"]}.\n\n'
                                             'При выборе жанра можно несколько раз нажимать на указанные'
                                             ' кнопки с цифрами, если Вы решили изменить свое решение. '
                                             'Если жанр выбран '
                                             'правильно - нажмите "В меню поиска" для настройки остальных фильтров',
                                     keyboard=keyboard)

                # Сообщение изменения сортировки
                if payload == 54:
                    send_message(peer_id=peer_id_in,
                                 message=f'В этом меню можно выбрать как будут отображаться фильмы и сериалы.\n\n'
                                         f'✅ 1) Сортировка по году - покажет список, который начинается с выбранного'
                                         f' Вами "Максимального году" и заканчивается выбранным Вами '
                                         f'"Минимальным годом". Все фильмы и сериалы будут отображены в '
                                         f'удобном для чтения порядке\n\n'
                                         f'✅ 2) Сортировка по рейтингу. Сортирует по рейтингу, выводит точно так же '
                                         f'как и при сортировке "По году". Фильмы и сериалы отображаются '
                                         f'так же в удобном порядке.\n\n'
                                         f'✅ 3) Сортировка по году и по рейтингу. Сортирует фильмы и сериалы для '
                                         f'каждого года по рейтингу. Например сначала выведутся все фильмы и сериалы '
                                         f'для 2020 года, сортированные по рейтингу, затем для 2019 и так далее. '
                                         f'Фильмы и сериалы отображаются так же в удобном порядке.\n\n'
                                         f'✅ 4) Сортировка по количеству голосов IMDB - Сортирует фильмы по количеству '
                                         f'оценок на сайте IMDB. Фильмы и сериалы отображаются так же в удобном порядке.',
                                 keyboard=keyboard)

                # Изменение сортировки
                elif payload in [70, 71, 72, 73]:
                    if payload == 70:
                        user_settings[user_id]["sorting"] = 'По году'
                    elif payload == 71:
                        user_settings[user_id]["sorting"] = 'По рейтингу'
                    elif payload == 72:
                        user_settings[user_id]["sorting"] = 'По году и рейтингу'
                    else:
                        user_settings[user_id]["sorting"] = 'По количеству голосов imdb'
                    send_message(peer_id=peer_id_in, message='Тип сортировки изменен на: '
                                                             f'{user_settings[user_id]["sorting"]}\n'
                                                             f'Изменить сортировку можно в этом же меню, для этого '
                                                             f'просто'
                                                             f' нажмите на нужную сортировку\n'
                                                             f'Для перехода обратно в меню фильтров нажмите '
                                                             f'"В меню поиска"'
                                                             f'',
                                 keyboard=keyboard)

                # Выбранные настройки
                if payload == 55:
                    send_message(peer_id=peer_id_in,
                                 message=f'✓Рейтинг от {user_settings[user_id]["min_rating"]} '
                                         f'до {user_settings[user_id]["max_rating"]}\n'
                                         f'✓Год от {user_settings[user_id]["start_year"]} '
                                         f'до {user_settings[user_id]["end_year"]}\n'
                                         f'✓Жанр - {user_settings[user_id]["first_genre"]}\n'
                                         f'✓Второй жанр - {user_settings[user_id]["second_genre"]}\n'
                                         f'✓Вид сортировки - {user_settings[user_id]["sorting"]}',
                                 keyboard=keyboard)

                # Количество отображаемых фильмов
                if payload == 543:
                    send_message(peer_id=peer_id_in, message='Выбери количество фильмов / сериалов, которое ты хочешь '
                                                             'увидеть после поиска',
                                 keyboard=keyboard)
                elif payload in [601, 602, 603, 604]:
                    user_settings[user_id]['count_for_films'] = payload

                vk.messages.markAsRead(peer_id=peer_id_in)

    except Exception as error:
        print(error)

