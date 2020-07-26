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
pemp = 'none'
kind_of_sorting = 'По кол-ву голосов imdb'
gen = 'Not now'
user_settings = {}


def our_keyboard():
    """Главное меню - начало диалога или любое сообщение """

    if payload is None or payload == 0:
        keyboard = VkKeyboard(one_time=False)
        # keyboard.add_button('Я уже знаю что посмотреть', payload=1, color=VkKeyboardColor.PRIMARY)
        # keyboard.add_line()
        keyboard.add_button('Я хочу выбрать рандомно', VkKeyboardColor.PRIMARY, payload=2)
        keyboard.add_line()
        keyboard.add_button('Продвинутый поиск', VkKeyboardColor.PRIMARY, payload=3)
        keyboard.add_line()
        keyboard.add_button('Топ 100 фильмов или сериалов', VkKeyboardColor.PRIMARY, payload=100)
        return keyboard.get_keyboard()

    elif payload == 2:
        """Главное меню - рандомный поиск """

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Фильм', VkKeyboardColor.PRIMARY, payload=5)
        keyboard.add_button('Сериал', VkKeyboardColor.PRIMARY, payload=6)
        keyboard.add_line()
        keyboard.add_button('Завершенный сериал', VkKeyboardColor.PRIMARY, payload=300)
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
        return keyboard.get_keyboard()

    elif payload == 3:
        """Главное меню - продвинутый поиск"""

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Выбрать год', VkKeyboardColor.PRIMARY, payload=19)
        keyboard.add_button('Выбрать рейтинг', VkKeyboardColor.PRIMARY, payload=20)
        keyboard.add_line()
        keyboard.add_button('Выбрать жанр', VkKeyboardColor.PRIMARY, payload=21)
        keyboard.add_button('Второй жанр', VkKeyboardColor.PRIMARY, payload=56)
        keyboard.add_line()
        keyboard.add_button('Выбрать сортировку', VkKeyboardColor.PRIMARY, payload=54)
        keyboard.add_line()
        keyboard.add_button('Выбранные настройки', VkKeyboardColor.DEFAULT, payload=55)
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
        return keyboard.get_keyboard()

    elif payload == 100 or payload in [61, 62, 63, 64, 65]:
        """Главное меню - топ 100 - меню выбора"""

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Топ 100 фильмов', VkKeyboardColor.PRIMARY, payload=61)
        keyboard.add_line()
        keyboard.add_button('Топ 100 сериалов', VkKeyboardColor.PRIMARY, payload=65)
        keyboard.add_line()
        keyboard.add_button('Топ 100 фильмов по одному жанру', VkKeyboardColor.PRIMARY, payload=64)
        keyboard.add_line()
        keyboard.add_button('Топ 100 сериалов по одному жанру', VkKeyboardColor.PRIMARY, payload=62)
        #keyboard.add_line()
        #keyboard.add_button('Топ 100 по году и рейтингу', VkKeyboardColor.PRIMARY, payload=63)
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
        return keyboard.get_keyboard()

    elif payload == 5 or payload == 6 or payload == 64 or payload == 300:
        """Цифры для выбора категории"""

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('1', VkKeyboardColor.PRIMARY, payload=7)
        keyboard.add_button('2', VkKeyboardColor.PRIMARY, payload=8)
        keyboard.add_button('3', VkKeyboardColor.PRIMARY, payload=9)
        keyboard.add_button('4', VkKeyboardColor.PRIMARY, payload=10)
        keyboard.add_line()
        keyboard.add_button('5', VkKeyboardColor.PRIMARY, payload=11)
        keyboard.add_button('6', VkKeyboardColor.PRIMARY, payload=12)
        keyboard.add_button('7', VkKeyboardColor.PRIMARY, payload=13)
        keyboard.add_button('8', VkKeyboardColor.PRIMARY, payload=14)
        keyboard.add_line()
        keyboard.add_button('9', VkKeyboardColor.PRIMARY, payload=15)
        keyboard.add_button('10', VkKeyboardColor.PRIMARY, payload=16)
        keyboard.add_button('11', VkKeyboardColor.PRIMARY, payload=17)
        keyboard.add_button('12', VkKeyboardColor.PRIMARY, payload=18)
        if payload == 5:
            keyboard.add_line()
            keyboard.add_button('Переключить на сериалы', VkKeyboardColor.DEFAULT, payload=6)
            keyboard.add_line()
            keyboard.add_button('Переключить на завершенные сериалы', VkKeyboardColor.DEFAULT, payload=300)
            keyboard.add_line()
            keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
            return keyboard.get_keyboard()
        elif payload == 6:
            keyboard.add_line()
            keyboard.add_button('Переключить на фильмы', VkKeyboardColor.DEFAULT, payload=5)
            keyboard.add_line()
            keyboard.add_button('Переключить на завершенные сериалы', VkKeyboardColor.DEFAULT, payload=300)
            keyboard.add_line()
            keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
            return keyboard.get_keyboard()
        elif payload == 300:
            keyboard.add_line()
            keyboard.add_button('Переключить на фильмы', VkKeyboardColor.DEFAULT, payload=5)
            keyboard.add_line()
            keyboard.add_button('Переключить на сериалы', VkKeyboardColor.DEFAULT, payload=6)
            keyboard.add_line()
            keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
            return keyboard.get_keyboard()
        else:
            keyboard.add_line()
            keyboard.add_button('Назад в меню поиска', VkKeyboardColor.PRIMARY, payload=3)
            keyboard.add_line()
            keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
            return keyboard.get_keyboard()

    elif payload == 19:
        """Продвинутый поиск - изменение года """

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Начальный год', VkKeyboardColor.PRIMARY, payload=23)
        keyboard.add_button('Конечный год', VkKeyboardColor.PRIMARY, payload=24)
        keyboard.add_line()
        keyboard.add_button('В меню поиска', VkKeyboardColor.PRIMARY, payload=3)
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
        return keyboard.get_keyboard()

    elif payload == 23 or payload == 24:
        """Выбор года для начального и конечного года"""

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('1989', VkKeyboardColor.PRIMARY, payload=201)
        keyboard.add_button('1990', VkKeyboardColor.PRIMARY, payload=202)
        keyboard.add_button('1991', VkKeyboardColor.PRIMARY, payload=203)
        keyboard.add_button('1992', VkKeyboardColor.PRIMARY, payload=204)
        keyboard.add_line()
        keyboard.add_button('1993', VkKeyboardColor.PRIMARY, payload=205)
        keyboard.add_button('1994', VkKeyboardColor.PRIMARY, payload=206)
        keyboard.add_button('1995', VkKeyboardColor.PRIMARY, payload=207)
        keyboard.add_button('1996', VkKeyboardColor.PRIMARY, payload=208)
        keyboard.add_line()
        keyboard.add_button('1997', VkKeyboardColor.PRIMARY, payload=209)
        keyboard.add_button('1998', VkKeyboardColor.PRIMARY, payload=210)
        keyboard.add_button('1999', VkKeyboardColor.PRIMARY, payload=211)
        keyboard.add_button('2000', VkKeyboardColor.PRIMARY, payload=212)
        keyboard.add_line()
        keyboard.add_button('2001', VkKeyboardColor.PRIMARY, payload=213)
        keyboard.add_button('2002', VkKeyboardColor.PRIMARY, payload=214)
        keyboard.add_button('2003', VkKeyboardColor.PRIMARY, payload=215)
        keyboard.add_button('2004', VkKeyboardColor.PRIMARY, payload=216)
        keyboard.add_line()
        keyboard.add_button('Следующая страница', VkKeyboardColor.PRIMARY, payload=99)
        if payload == 23:
            keyboard.add_line()
            keyboard.add_button('Переключить на конечный год', VkKeyboardColor.DEFAULT, payload=24)
            keyboard.add_line()
        elif payload == 24:
            keyboard.add_line()
            keyboard.add_button('Переключить на начальный год', VkKeyboardColor.DEFAULT, payload=23)
            keyboard.add_line()
        keyboard.add_button('В меню поиска', VkKeyboardColor.DEFAULT, payload=3)
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
        return keyboard.get_keyboard()

    elif payload == 99 or payload in [23, 24]:
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('2005', VkKeyboardColor.PRIMARY, payload=217)
        keyboard.add_button('2006', VkKeyboardColor.PRIMARY, payload=218)
        keyboard.add_button('2007', VkKeyboardColor.PRIMARY, payload=219)
        keyboard.add_button('2008', VkKeyboardColor.PRIMARY, payload=220)
        keyboard.add_line()
        keyboard.add_button('2009', VkKeyboardColor.PRIMARY, payload=221)
        keyboard.add_button('2010', VkKeyboardColor.PRIMARY, payload=222)
        keyboard.add_button('2011', VkKeyboardColor.PRIMARY, payload=223)
        keyboard.add_button('2012', VkKeyboardColor.PRIMARY, payload=224)
        keyboard.add_line()
        keyboard.add_button('2013', VkKeyboardColor.PRIMARY, payload=225)
        keyboard.add_button('2014', VkKeyboardColor.PRIMARY, payload=226)
        keyboard.add_button('2015', VkKeyboardColor.PRIMARY, payload=227)
        keyboard.add_button('2016', VkKeyboardColor.PRIMARY, payload=228)
        keyboard.add_line()
        keyboard.add_button('2017', VkKeyboardColor.PRIMARY, payload=229)
        keyboard.add_button('2018', VkKeyboardColor.PRIMARY, payload=230)
        keyboard.add_button('2019', VkKeyboardColor.PRIMARY, payload=231)
        keyboard.add_button('2020', VkKeyboardColor.PRIMARY, payload=232)
        keyboard.add_line()
        keyboard.add_button('Предыдущая страница', VkKeyboardColor.PRIMARY, payload=23)
        if pemp == 'start':
            keyboard.add_line()
            keyboard.add_button('Переключить на конечный год', VkKeyboardColor.DEFAULT, payload=24)
            keyboard.add_line()
        elif pemp == 'end':
            keyboard.add_line()
            keyboard.add_button('Переключить на начальный год', VkKeyboardColor.DEFAULT, payload=23)
            keyboard.add_line()
        keyboard.add_button('В меню поиска', VkKeyboardColor.DEFAULT, payload=3)
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
        return keyboard.get_keyboard()

    elif payload == 20:
        """Продвинутый поиск - изменение рейтинга """

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Мин. рейтинг', VkKeyboardColor.PRIMARY, payload=25)
        keyboard.add_button('Макс. рейтинг', VkKeyboardColor.PRIMARY, payload=26)
        keyboard.add_line()
        keyboard.add_button('В меню поиска', VkKeyboardColor.PRIMARY, payload=3)
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
        return keyboard.get_keyboard()

    elif payload == 21:
        """Продвинутый поиск - изменение жанра """

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('1', VkKeyboardColor.PRIMARY, payload=27)
        keyboard.add_button('2', VkKeyboardColor.PRIMARY, payload=28)
        keyboard.add_button('3', VkKeyboardColor.PRIMARY, payload=29)
        keyboard.add_button('4', VkKeyboardColor.PRIMARY, payload=30)
        keyboard.add_line()
        keyboard.add_button('5', VkKeyboardColor.PRIMARY, payload=31)
        keyboard.add_button('6', VkKeyboardColor.PRIMARY, payload=32)
        keyboard.add_button('7', VkKeyboardColor.PRIMARY, payload=33)
        keyboard.add_button('8', VkKeyboardColor.PRIMARY, payload=34)
        keyboard.add_line()
        keyboard.add_button('9', VkKeyboardColor.PRIMARY, payload=35)
        keyboard.add_button('10', VkKeyboardColor.PRIMARY, payload=36)
        keyboard.add_button('11', VkKeyboardColor.PRIMARY, payload=37)
        keyboard.add_button('12', VkKeyboardColor.PRIMARY, payload=38)
        keyboard.add_line()
        keyboard.add_button('Выбрать второй жанр', VkKeyboardColor.DEFAULT, payload=56)
        keyboard.add_line()
        keyboard.add_button('В меню поиска', VkKeyboardColor.DEFAULT, payload=3)
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
        return keyboard.get_keyboard()

    if payload == 56:
        """Продвинутый поиск - изменение жанра """

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('1', VkKeyboardColor.PRIMARY, payload=27)
        keyboard.add_button('2', VkKeyboardColor.PRIMARY, payload=28)
        keyboard.add_button('3', VkKeyboardColor.PRIMARY, payload=29)
        keyboard.add_button('4', VkKeyboardColor.PRIMARY, payload=30)
        keyboard.add_line()
        keyboard.add_button('5', VkKeyboardColor.PRIMARY, payload=31)
        keyboard.add_button('6', VkKeyboardColor.PRIMARY, payload=32)
        keyboard.add_button('7', VkKeyboardColor.PRIMARY, payload=33)
        keyboard.add_button('8', VkKeyboardColor.PRIMARY, payload=34)
        keyboard.add_line()
        keyboard.add_button('9', VkKeyboardColor.PRIMARY, payload=35)
        keyboard.add_button('10', VkKeyboardColor.PRIMARY, payload=36)
        keyboard.add_button('11', VkKeyboardColor.PRIMARY, payload=37)
        keyboard.add_button('12', VkKeyboardColor.PRIMARY, payload=38)
        keyboard.add_line()
        keyboard.add_button('Выбрать первый жанр', VkKeyboardColor.DEFAULT, payload=21)
        keyboard.add_line()
        keyboard.add_button('В меню поиска', VkKeyboardColor.DEFAULT, payload=3)
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
        return keyboard.get_keyboard()

    elif payload == 25 or payload == 26 or payload in [39, 40, 41, 42, 43, 44, 45, 46, 47, 48]:
        """Продвинутый поиск - меню для изменение рейтинга """

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('1', VkKeyboardColor.PRIMARY, payload=39)
        keyboard.add_button('2', VkKeyboardColor.PRIMARY, payload=40)
        keyboard.add_button('3', VkKeyboardColor.PRIMARY, payload=41)
        keyboard.add_button('4', VkKeyboardColor.PRIMARY, payload=42)
        keyboard.add_line()
        keyboard.add_button('5', VkKeyboardColor.PRIMARY, payload=43)
        keyboard.add_button('6', VkKeyboardColor.PRIMARY, payload=44)
        keyboard.add_button('7', VkKeyboardColor.PRIMARY, payload=45)
        keyboard.add_button('8', VkKeyboardColor.PRIMARY, payload=46)
        keyboard.add_line()
        keyboard.add_button('9', VkKeyboardColor.PRIMARY, payload=47)
        keyboard.add_button('10', VkKeyboardColor.PRIMARY, payload=48)
        if temp == 'min' or payload == 25:
            keyboard.add_line()
            keyboard.add_button('Переключить на макс. рейтинг', VkKeyboardColor.DEFAULT, payload=26)
            keyboard.add_line()
        elif temp == 'max' or payload == 26:
            keyboard.add_line()
            keyboard.add_button('Переключить на мин. рейтинг', VkKeyboardColor.DEFAULT, payload=25)
            keyboard.add_line()
        keyboard.add_button('В меню поиска', VkKeyboardColor.DEFAULT, payload=3)
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
        return keyboard.get_keyboard()

    elif payload == 54 or payload in [70, 71, 72, 73]:
        """Продвинутый поиск - выбор сортировки"""
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('По году', payload=70, color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('По рейтингу', VkKeyboardColor.PRIMARY, payload=71)
        keyboard.add_line()
        keyboard.add_button('По году и рейтингу', VkKeyboardColor.PRIMARY, payload=72)
        keyboard.add_line()
        keyboard.add_button('По кол-ву голосов imdb', VkKeyboardColor.PRIMARY, payload=73)
        keyboard.add_line()
        keyboard.add_button('В меню поиска', VkKeyboardColor.DEFAULT, payload=3)
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
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

    def set_settings(self, user_id_class, st_year, en_year, mn_rating, mx_rating, fs_genre, sc_genre, sort, users_s):
        self.start_year = st_year,
        self.end_year = en_year,
        self.min_rating = mn_rating,
        self.max_rating = mx_rating,
        self.first_genre = fs_genre,
        self.second_genre = sc_genre,
        self.sorting = sort
        users_s[user_id_class] = {
            'start_year': self.start_year[0],
            'end_year': self.end_year[0],
            'min_rating': self.min_rating[0],
            'max_rating': self.max_rating[0],
            'first_genre': self.first_genre[0],
            'second_genre': self.second_genre[0],
            'sorting': self.sorting
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

                if user_settings.get(user_id) == None:
                    user = SetSettings(user_id)
                    user.set_settings(user_id, min_year, max_year, min_rating, max_rating, genre_id,
                                                        second_genre_id, kind_of_sorting, user_settings)

                try:
                    if event.obj['message']['payload'] != None:
                        payload = int(event.obj['message']['payload'])
                    else:
                        payload = None

                except Exception as error1:
                    print(error1)
                    payload = None

                keyboard = our_keyboard()

                # Если сообщение пустое
                if payload is None:
                    send_message(peer_id=peer_id_in, message='Мы в главном меню', keyboard=keyboard)




                # Рандомный поиск
                elif payload == 2:
                    send_message(peer_id=peer_id_in, message='Для рандомного выбора нужно выбрать категорию:',
                                 keyboard=keyboard)
                # Выбор жанра
                elif payload == 5 or payload == 6 or payload == 300:
                    temp = 'basic'
                    send_message(peer_id=peer_id_in, message='Теперь нужно выбрать жанр:\n'
                                                             f'{category_list}',
                                 keyboard=keyboard)
                    film_or_serial = payload

                # Если ответ на выбор жанра правильный и есть в списке
                if payload in [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18] and temp == 'basic':
                    genre_id = payload - 6

                    # Подбор рандомного фильма
                    if film_or_serial == 5:
                        db = get_connection()
                        cursor = db.cursor()
                        selector_for_genre = ('SELECT * FROM genre_movie WHERE genre_id = %s')
                        cursor.execute(selector_for_genre, (genre_id,))
                        films_for_categories = [x[1] for x in cursor.fetchall()]
                        random_film = random.choices(films_for_categories)
                        while True:
                            selector = (
                                'SELECT * FROM movie WHERE premier > 2001 and rating > 6 and type_id = 0 and duration > 0 and votes > 25000 and id = %s')
                            film = random_film[0]
                            cursor.execute(selector, (film,))
                            checker = cursor.fetchall()
                            if len(checker) > 0:
                                prod_actor_genre = actors_producers_genres(film)
                                our_film = f"---Фильм---\n▶{checker[0][1]}\n\n✓Жанры - {prod_actor_genre[2]}" \
                                           f"\n✓Год премьеры - {checker[0][3]}\n✓Рейтинг - " \
                                           f"{checker[0][5]}\n✓Продолжительность - {checker[0][6]} мин\n" \
                                           f"✓Количество голосов imdb - {checker[0][7]}\n\n" \
                                           f"🎬Продюсер - {prod_actor_genre[0]}\n✪Актеры - {prod_actor_genre[1]}\n\n" \
                                           f"Ссылка  - {checker[0][8]}"
                                break
                            else:
                                random_film = random.choices(films_for_categories)

                        send_message(peer_id=peer_id_in, message='А вот и твой фильм:\n'
                                                                 f'{our_film}',
                                     keyboard=keyboard)

                    # Подбор рандомного сериала
                    elif film_or_serial == 6:
                        db = get_connection()
                        cursor = db.cursor()
                        selector_for_genre = ('SELECT * FROM genre_movie WHERE genre_id = %s')
                        cursor.execute(selector_for_genre, (genre_id,))
                        films_for_categories = [x[1] for x in cursor.fetchall()]
                        random_film = random.choices(films_for_categories)
                        while True:
                            selector = (
                                'SELECT * FROM movie WHERE premier > 2001 and rating > 6 and type_id = 1 and votes > 25000 and duration > 0 and id = %s')
                            film = random_film[0]
                            cursor.execute(selector, (film,))
                            checker = cursor.fetchall()
                            if len(checker) > 0:
                                prod_actor_genre = actors_producers_genres(film)
                                our_film = f"---Сериал---\n▶{checker[0][1]}\n\n✓Жанры - {prod_actor_genre[2]}" \
                                           f"\n✓Год премьеры - {checker[0][3]}\n✓Рейтинг - " \
                                           f"{checker[0][5]}\n✓Продолжительность - {checker[0][6]} мин\n" \
                                           f"✓Количество голосов imdb - {checker[0][7]}\n\n" \
                                           f"🎬Продюсер - {prod_actor_genre[0]}\n✪Актеры - {prod_actor_genre[1]}\n\n" \
                                           f"Ссылка  - {checker[0][8]}"
                                break
                            else:
                                random_film = random.choices(films_for_categories)
                        send_message(peer_id=peer_id_in, message='А вот и твой сериал:\n'
                                                                 f'{our_film}',
                                     keyboard=keyboard)

                    elif film_or_serial == 300:
                        db = get_connection()
                        cursor = db.cursor()
                        selector_for_genre = ('SELECT * FROM genre_movie WHERE genre_id = %s')
                        cursor.execute(selector_for_genre, (genre_id,))
                        films_for_categories = [x[1] for x in cursor.fetchall()]
                        random_film = random.choices(films_for_categories)
                        while True:
                            selector = ('SELECT * FROM movie WHERE premier > 2001 and rating > 6 and type_id = 2 and votes > 25000 and duration > 0 and id = %s')
                            film = random_film[0]
                            cursor.execute(selector, (film,))
                            checker = cursor.fetchall()
                            if len(checker) > 0:
                                prod_actor_genre = actors_producers_genres(film)
                                our_film = f"---Сериал---\n▶{checker[0][1]}\n\n✓Жанры - {prod_actor_genre[2]}" \
                                           f"\n✓Год премьеры - {checker[0][3]}\n✓Последней сезон - {checker[0][4]}" \
                                           f"\n✓Рейтинг - " \
                                           f"{checker[0][5]}\n✓Продолжительность - {checker[0][6]} мин\n" \
                                           f"✓Количество голосов imdb - {checker[0][7]}\n\n" \
                                           f"🎬Продюсер - {prod_actor_genre[0]}\n✪Актеры - {prod_actor_genre[1]}\n\n" \
                                           f"Ссылка  - {checker[0][8]}"
                                break
                            else:
                                random_film = random.choices(films_for_categories)
                        send_message(peer_id=peer_id_in, message='А вот и твой сериал:\n'
                                                                 f'{our_film}',
                                     keyboard=keyboard)





                # Продвинутый поиск
                elif payload == 3:
                    send_message(peer_id=peer_id_in, message='В меню продвинутого поиска: ',
                                 keyboard=keyboard)

                # Изменяем год - исправить
                elif payload == 19:
                    send_message(peer_id=peer_id_in, message='Меню изменения года',
                                 keyboard=keyboard)

                # Меню выбора года для поиска
                elif payload == 23:
                    pemp = 'start'
                    send_message(peer_id=peer_id_in, message='Выбираем минимальный год: ',
                                 keyboard=keyboard)

                elif payload == 24:
                    pemp = 'end'
                    send_message(peer_id=peer_id_in, message='Выбираем максимальный год: ',
                                 keyboard=keyboard)

                # Проверяем выбранный год
                elif payload in [201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217,
                               218, 219,
                               220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232]:

                    if pemp == 'start':
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

                    elif pemp == 'end':
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

                elif payload == 99:
                    send_message(peer_id=peer_id_in, message='Открываем следующую страницу: ',
                                 keyboard=keyboard)




                # Изменяем рейтинг
                elif payload == 20:
                    send_message(peer_id=peer_id_in, message='Меню изменения рейтинга',
                                 keyboard=keyboard)

                # Изменяем выбираем жанр
                elif payload == 21:
                    gen = 'first'
                    temp = 'for_21'
                    send_message(peer_id=peer_id_in, message='Теперь нужно выбрать жанр:\n'
                                                             f'{category_list}',
                                 keyboard=keyboard)

                # Если ответ по жанру есть в списке - присваиваем жанр. Temp - различие для клавиатуры
                elif payload in [27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38] and gen == 'first':
                    user_settings[user_id]["first_genre"] = list_of_genres[payload - 26]["Genre name"]
                    send_message(peer_id=peer_id_in,
                                 message=f'Жанр был успешно выбран - '
                                         f'{user_settings[user_id]["first_genre"]}.\n\n'
                                         'При выборе жанра можно несколько раз нажимать на указанные'
                                         ' кнопки с цифрами, если Вы решили изменить свое решение. Если же жанр выбран'
                                         ' правильно - можно вернуться к настройкам остальных фильтров нажам на '
                                         '"В меню поиска"',
                                 keyboard=keyboard)

                # Клавиатура для изменения рейтинга
                elif payload == 25 or payload == 26:
                    if payload == 25:
                        temp = 'min'
                        send_message(peer_id=peer_id_in, message='В меню изменения начального рейтинга',
                                     keyboard=keyboard)
                    elif payload == 26:
                        temp = 'max'
                        send_message(peer_id=peer_id_in, message='В меню изменения конечного рейтинга',
                                     keyboard=keyboard)

                # Если число по рейтингу есть - присваиваем значения min_rating и max_rating
                if payload in [39, 40, 41, 42, 43, 44, 45, 46, 47, 48]:
                    if temp == 'min':
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

                    elif temp == 'max':
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


                # Выбор сортировки
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


                # Определяем как будем сортировать
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

                if payload == 56:
                    gen = 'second'
                    temp = 'for_56'
                    send_message(peer_id=peer_id_in, message='Теперь нужно выбрать жанр:\n'
                                                             f'{category_list}',
                                 keyboard=keyboard)

                # Если ответ по жанру есть в списке - присваиваем жанр. Temp - различие для клавиатуры
                elif payload in [27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38] and gen == 'second':
                    user_settings[user_id]["second_genre"] = list_of_genres[payload - 26]["Genre name"]
                    send_message(peer_id=peer_id_in,
                                 message=f'Второй жанр был успешно выбран - '
                                         f'{user_settings[user_id]["second_genre"]}.\n\n'
                                         'При выборе жанра можно несколько раз нажимать на указанные'
                                         ' кнопки с цифрами, если Вы решили изменить свое решение. Если жанр выбран '
                                         'правильно - нажмите "В меню поиска" для настройки остальных фильтров',
                                 keyboard=keyboard)

                if payload == 100:
                    send_message(peer_id=peer_id_in, message='Меню топов',
                                 keyboard=keyboard)

                # Выводим топ 100 фильмов и топ 100 сериалов по всем жанрам
                elif payload in [61, 62, 63, 64, 65]:
                    if payload == 61:
                        film_counter = 1
                        selector_for_100_films = 'SELECT * FROM top_250_movie'
                        db_100 = get_connection()
                        cursor_100 = db_100.cursor()
                        cursor_100.execute(selector_for_100_films)
                        answer = ''
                        count = 0
                        for film in cursor_100.fetchall():
                            answer += f"{film_counter}-----{film[1]}-----\n"
                            answer += f'✓Жанры: {film[2]}\n'
                            answer += f'✓Рейтинг: {film[3]}\n'
                            answer += f'✓Год: {film[4]}\n'
                            answer += f'✓Количество голосов: {film[-1]}\n\n'
                            count += 1
                            film_counter += 1
                            if count == 25:
                                count = 0
                                send_message(peer_id=peer_id_in, message=f'{answer}',
                                             keyboard=keyboard)
                                answer = ''
                            if film_counter > 100:
                                break

                    elif payload == 65:
                        serial_counter = 1
                        selector_for_100_serials = 'SELECT * FROM top_250_serials'
                        db_1005 = get_connection()
                        cursor_1005 = db_1005.cursor()
                        cursor_1005.execute(selector_for_100_serials)
                        answer2 = ''
                        count1 = 0
                        for film in cursor_1005.fetchall():
                            answer2 += f"{serial_counter}-----{film[1]}-----\n"
                            answer2 += f'✓Жанры: {film[2]}\n'
                            answer2 += f'✓Рейтинг: {film[3]}\n'
                            answer2 += f'✓Год: {film[4]}\n'
                            answer2 += f'✓Количество голосов: {film[-1]}\n\n'
                            count1 += 1
                            serial_counter += 1
                            if count1 == 25:
                                count1 = 0
                                send_message(peer_id=peer_id_in, message=f'{answer2}',
                                             keyboard=keyboard)
                                answer2 = ''
                            if serial_counter > 100:
                                break

                # Показать выбранную настройку
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

                vk.messages.markAsRead(peer_id=peer_id_in)

    except Exception as error:
        print(error)