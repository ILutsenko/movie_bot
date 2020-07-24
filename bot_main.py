import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboardColor, VkKeyboardButton, VkKeyboard
import mysql.connector
import random
from bot_genres import category_list, list_of_genres
from datetime import datetime
from kinopoisk.movie import Movie


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


def key_advanced():
    if payload == 19:
        """Продвинутый поиск - изменение года """

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Начальный год', VkKeyboardColor.PRIMARY, payload=23)
        keyboard.add_button('Конечный год', VkKeyboardColor.PRIMARY, payload=24)
        keyboard.add_line()
        keyboard.add_button('В меню поиска', VkKeyboardColor.PRIMARY, payload=3)
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
        return keyboard.get_keyboard()

    if payload == 23 or payload == 24:
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
        keyboard.add_button('Следующая страница', VkKeyboardColor.DEFAULT, payload=99)
        keyboard.add_line()
        keyboard.add_button('Назад', VkKeyboardColor.PRIMARY, payload=19)
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
        return keyboard.get_keyboard()

    if payload == 99:
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
        keyboard.add_line()
        keyboard.add_button('Назад', VkKeyboardColor.PRIMARY, payload=19)
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
        keyboard.add_button('Назад', VkKeyboardColor.PRIMARY, payload=3)
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
        return keyboard.get_keyboard()

    if payload == 25 or payload == 26 or payload in [39, 40, 41, 42, 43, 44, 45, 46, 47, 48]:
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
        keyboard.add_line()
        keyboard.add_button('Назад', VkKeyboardColor.PRIMARY, payload=20)
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
        return keyboard.get_keyboard()

    if payload == 54 or payload in [70, 71, 72, 73]:
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

    if payload == 100:
        """Топ 100 - меню выбора"""
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Топ 100 по всем жанрам', VkKeyboardColor.PRIMARY, payload=61)
        keyboard.add_line()
        keyboard.add_button('Топ 100 по одному жанру', VkKeyboardColor.PRIMARY, payload=64)
        keyboard.add_line()
        keyboard.add_button('Топ 100 по рейтингу', VkKeyboardColor.PRIMARY, payload=62)
        keyboard.add_line()
        keyboard.add_button('Топ 100 по году и рейтингу', VkKeyboardColor.PRIMARY, payload=63)
        keyboard.add_line()
        keyboard.add_button('Топ 100 сериалов', VkKeyboardColor.PRIMARY, payload=65)
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
        return keyboard.get_keyboard()


def start_menu():
    """Главное меню - начало диалога или любое сообщение """

    if payload is None or payload == 0:
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Я уже знаю что посмотреть', payload=1, color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Я хочу выбрать рандомно', VkKeyboardColor.PRIMARY, payload=2)
        keyboard.add_line()
        keyboard.add_button('Продвинутый поиск', VkKeyboardColor.PRIMARY, payload=3)
        keyboard.add_line()
        keyboard.add_button('Топ 100 фильмов и сериалов по жанрам', VkKeyboardColor.PRIMARY, payload=100)
        return keyboard.get_keyboard()

    if payload == 1:
        """Главное меню - я знаю что буду искать """
        pass

    elif payload == 2:
        """Главное меню - рандомный поиск """

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Фильм', VkKeyboardColor.PRIMARY, payload=5)
        keyboard.add_button('Сериал', VkKeyboardColor.PRIMARY, payload=6)
        keyboard.add_line()
        keyboard.add_button('Главное меню', VkKeyboardColor.PRIMARY, payload=0)
        return keyboard.get_keyboard()

    elif payload == 3:
        """Главное меню - продвинутый поиск"""

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Выбрать год', VkKeyboardColor.PRIMARY, payload=19)
        keyboard.add_line()
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

    if payload == 5 or payload == 6 or payload == 21 or payload == 56 or payload == 64:
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
            keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
            return keyboard.get_keyboard()
        elif payload == 6:
            keyboard.add_line()
            keyboard.add_button('Переключить на фильмы', VkKeyboardColor.DEFAULT, payload=5)
            keyboard.add_line()
            keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
            return keyboard.get_keyboard()
        else:
            keyboard.add_line()
            keyboard.add_button('Назад в меню поиска', VkKeyboardColor.PRIMARY, payload=3)
            keyboard.add_line()
            keyboard.add_button('Главное меню', VkKeyboardColor.DEFAULT, payload=0)
            return keyboard.get_keyboard()


VK_API_VERSION = '5.120'
GROUP_ID = 197300375
VK_API_ACCESS_TOKEN = '50b21743f85bf752ccb5a0f29a1009e0f7bac25bbd6e0ef9211acb4fdb33bb1d5f11099497f14409c561c'


vk_session = vk_api.VkApi(token=VK_API_ACCESS_TOKEN)
vk = vk_session.get_api()

# Первый запрос к LongPoll: получаем server и key
longpoll = VkBotLongPoll(vk_session, 197300375)

# Переменные
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

        try:
            if event.obj['message']['payload'] != None:
                payload = int(event.obj['message']['payload'])
            else:
                payload = None
        except:
            payload = None

        keyboard = start_menu()
        # Начало диалога или любое сообщение
        if payload == None:
            send_message(peer_id=peer_id_in, message='Мы в главном меню', keyboard=keyboard)

        # Рандомный поиск
        elif payload == 2:
            send_message(peer_id=peer_id_in, message='Для рандомного выбора нужно выбрать категорию:',
                         keyboard=keyboard)
        # Продвинутый поиск
        elif payload == 3:
            send_message(peer_id=peer_id_in, message='В меню продвинутого поиска: ',
                         keyboard=keyboard)

        elif payload == 100:
            temp = 'top100'
            send_message(peer_id=peer_id_in, message='Теперь нужно выбрать жанр:\n'
                                                     f'{category_list}',
                         keyboard=keyboard)

        if payload in [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18] and temp == 'top100':
            key_advanced = key_advanced()
            genre_id_for_top_100 = payload - 6
            send_message(peer_id=peer_id_in, message='Жанр для топ 100 успешно выбран:\n', keyboard=key_advanced)

        # Отображение топ 100 фильмов
        if payload == 61 or payload == 62 or payload == 63:
            if payload == 61:
                pass
            elif payload == 62:
                pass
            else:
                pass

        # Выбор жанра
        elif payload == 5 or payload == 6:
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
                cursor.execute(selector_for_genre, (genre_id, ))
                films_for_categories = [x[1] for x in cursor.fetchall()]
                random_film = random.choices(films_for_categories)
                while True:
                    selector = ('SELECT * FROM movie WHERE premier > 2001 and rating > 6 and type_id = 0 and duration > 0 and votes > 25000 and id = %s')
                    film = random_film[0]
                    cursor.execute(selector, (film, ))
                    checker = cursor.fetchall()
                    if len(checker) > 0:
                        prod_actor_genre = actors_producers_genres(film)
                        our_film = f"Название фильма - {checker[0][1]}\nЖанры - {prod_actor_genre[2]}" \
                                   f"\nГод премьеры - {checker[0][3]}\nРейтинг - " \
                                   f"{checker[0][5]}\nПродюсер - {prod_actor_genre[0]}\nАктеры - {prod_actor_genre[1]}" \
                                   f"\nПродолжительность - {checker[0][6]} мин\n" \
                                   f" Количество голосов imdb - {checker[0][7]} голосов\nСсылка  - {checker[0][8]}"
                        break
                    else:
                        random_film = random.choices(films_for_categories)

                send_message(peer_id=peer_id_in, message='Окей, вот твой фильм:\n'
                                                         f'{our_film}',
                             keyboard=keyboard)

            # Подбор рандомного сериала
            elif film_or_serial == 6:
                db = get_connection()
                cursor = db.cursor()
                selector_for_genre = ('SELECT * FROM genre_movie WHERE genre_id = %s')
                cursor.execute(selector_for_genre, (genre_id, ))
                films_for_categories = [x[1] for x in cursor.fetchall()]
                random_film = random.choices(films_for_categories)
                while True:
                    selector = ('SELECT * FROM movie WHERE premier > 2001 and rating > 6 and type_id = 1 and votes > 25000 and duration > 0 and id = %s')
                    film = random_film[0]
                    cursor.execute(selector, (film,))
                    checker = cursor.fetchall()
                    if len(checker) > 0:
                        prod_actor_genre = actors_producers_genres(film)
                        our_film = f"Название фильма - {checker[0][1]}\nЖанры - {prod_actor_genre[2]}" \
                                   f"\nГод премьеры - {checker[0][3]}\nРейтинг - " \
                                   f"{checker[0][5]}\nПродюсер - {prod_actor_genre[0]}\nАктеры - {prod_actor_genre[1]}" \
                                   f"\nПродолжительность серии - {checker[0][6]} мин\n" \
                                   f" Количество голосов imdb - {checker[0][7]} голосов\nСсылка  - {checker[0][8]}"
                        break
                    else:
                        random_film = random.choices(films_for_categories)
                send_message(peer_id=peer_id_in, message='Окей, вот твой сериал:\n'
                                                         f'{our_film}',
                             keyboard=keyboard)

        """Продвинутый поиск"""
        keyboard2 = key_advanced()

        # Изменяем год
        if payload == 19:
            send_message(peer_id=peer_id_in, message='Автоматически минимальный год выставлен на 2000, а '
                                                     'максимальный - на 2020. Получается такой формат: '
                                                     'от 2010 до 2020.\n'
                                                     'Это можно '
                                                     'изменить здесь, а можно оставить как есть и вернуться '
                                                     'к остальным фильтрам. \n\n'
                                                     'При выборе года можно несколько раз нажимать на указанные'
                                                     ' кнопки с цифрами, если Вы решили изменить свое решение',
                         keyboard=keyboard2)

        # Меню выбора года для поиска
        if payload == 23:
            keyboard_func = key_advanced()
            pemp = 'start'
            send_message(peer_id=peer_id_in, message='Окей, выбираем минимальный год: ',
                         keyboard=keyboard_func)
        elif payload == 24:
            keyboard_func = key_advanced()
            pemp = 'end'
            send_message(peer_id=peer_id_in, message='Окей, выбираем максимальный год: ',
                         keyboard=keyboard_func)

        # Проверяем выбранный год
        if payload in [201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219,
                       220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232]:
            if pemp == 'start':
                min_year = payload + 1788
                send_message(peer_id=peer_id_in, message=f'Минимальный год успешно выбран - {min_year}')
            elif pemp == 'end':
                max_year = payload + 1788
                send_message(peer_id=peer_id_in, message=f'Максимальный год успешно выбран - {max_year}')

        if payload == 99:
            keyboard_func = key_advanced()
            send_message(peer_id=peer_id_in, message='Открываем следующую страницу: ',
                         keyboard=keyboard_func)

        # Изменяем рейтинг
        elif payload == 20:
            send_message(peer_id=peer_id_in, message='Автоматически минимальный рейтинг выставлен на 6, а '
                                                     'максимальный - на 10. Получается такой формат: '
                                                     'от 6 до 10'
                                                     'Это можно '
                                                     'изменить здесь, а можно оставить как есть и вернуться '
                                                     'к остальным фильтрам. \n\n'
                                                     'При выборе рейтинга можно несколько раз нажимать на указанные'
                                                     ' кнопки с цифрами, если Вы решили изменить свое решение',
                         keyboard=keyboard2)

        # Изменяем выбираем жанр
        elif payload == 21:
            temp = 'for_21'
            send_message(peer_id=peer_id_in, message='Теперь нужно выбрать жанр:\n'
                                                     f'{category_list}',
                         keyboard=keyboard)

        # Если ответ по жанру есть в списке - присваиваем жанр. Temp - различие для клавиатуры
        elif payload in [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18] and temp == 'for_21':
            genre_id = payload - 6
            send_message(peer_id=peer_id_in,
                         message=f'Жанр был успешно выбран - {list_of_genres[genre_id]["Genre name"]}.\n\n'
                                 'При выборе жанра можно несколько раз нажимать на указанные'
                                 ' кнопки с цифрами, если Вы решили изменить свое решение',
                         keyboard=keyboard2)

        # Клавиатура для изменения рейтинга
        elif payload == 25 or payload == 26:
            if payload == 25:
                temp = 'min'
                send_message(peer_id=peer_id_in, message='Автоматически минимальный рейтинг выставлен на 6,'
                                                         ' но это можно '
                                                         'изменить здесь, а можно оставить как есть и вернуться '
                                                         'к остальным фильтрам. \n\n'
                                                         'При выборе рейтинга можно несколько раз нажимать на указанные'
                                                         ' кнопки с цифрами, если Вы решили изменить свое решение',
                             keyboard=keyboard2)
            elif payload == 26:
                temp = 'max'
                send_message(peer_id=peer_id_in, message='Автоматически максимальный рейтинг выставлен на 10, '
                                                         ' но это можно '
                                                         'изменить здесь, а можно оставить как есть и вернуться '
                                                         'к остальным фильтрам. \n\n'
                                                         'При выборе рейтинга можно несколько раз нажимать на указанные'
                                                         ' кнопки с цифрами, если Вы решили изменить свое решение',
                             keyboard=keyboard2)

        # Если число по рейтингу есть - присваиваем значения min_rating и max_rating
        if payload in [39, 40, 41, 42, 43, 44, 45, 46, 47, 48]:
            if temp == 'min':
                min_rating = payload - 38
                send_message(peer_id=peer_id_in,
                             message=f'Минимальный рейтинг успешно изменен на {min_rating}\n'
                                     f'Можно вернуться в меню поиска чтобы настроить остальные фильтры или выбрать '
                                     f'рейтинг еще раз из этого меню, просто нажав на цифру',
                             keyboard=keyboard2)

            elif temp == 'max':
                max_rating = payload - 38
                send_message(peer_id=peer_id_in,
                             message=f'Максимальный рейтинг успешно изменен на {max_rating}\n'
                                     f'Можно вернуться в меню поиска чтобы настроить остальные фильтры или выбрать '
                                     f'рейтинг еще раз из этого меню, просто нажав на цифру',
                             keyboard=keyboard2)
        if payload == 55:
                try:
                    genre_id = int(genre_id)
                    genre_id_for_answer = list_of_genres[genre_id]["Genre name"]
                except:
                    genre_id_for_answer = 'Не выбран'

                try:
                    second_genre_id = int(second_genre_id)
                    second_genre_id_for_answer = list_of_genres[second_genre_id]['Genre name']
                except:
                    second_genre_id_for_answer = 'Не выбран'

                send_message(peer_id=peer_id_in,
                             message=f'Рейтинг от {min_rating} до {max_rating}\n'
                                     f'Год от {min_year} до {max_year}\n'
                                     f'Жанр - {genre_id_for_answer}\n'
                                     f'Второй жанр - {second_genre_id_for_answer}\n'
                                     f'Вид сортировки - {kind_of_sorting}',
                             keyboard=keyboard2)

        if payload == 54:
            send_message(peer_id=peer_id_in,
                         message=f'В этом меню можно выбрать как будут отображаться фильмы или сериалы сверху - вниз\n'
                                 f'По умолчанию сортировка задана по количеству голосов imdb\n'
                                 f'1) Сортировка по году - от выбранного Вами года, например от 2020,'
                                 f' до выбранного минимального года, например до 2015.\n\n'
                                 f'2) Сортировка по рейтингу выстроит фильмы или сериалы по рейтингу, от'
                                 f' большего рейтинга'
                                 f'к меньшиму.\n\n'
                                 f'3) Сортировка по году и рейтингу отсортирует для каждого года'
                                 f' по рейтингу, так же сверху вниз.\n\n'
                                 f'4) Сортировка по количеству голосов - соответственно сверху вниз',
                         keyboard=keyboard2)

        elif payload in [70, 71, 72, 73]:
            if payload == 70:
                kind_of_sorting = 'По году'
            elif payload == 71:
                kind_of_sorting = 'По рейтингу'
            elif payload == 72:
                kind_of_sorting = 'По году и рейтингу'
            else:
                kind_of_sorting = 'По количеству голосов imdb'
            send_message(peer_id=peer_id_in, message='Тип сортировки изменен на: '
                                                     f'{kind_of_sorting}\n'
                                                     f'Изменить сортировку можно в этом же меню, для этого просто'
                                                     f' нажмите на нужную сортировку\n'
                                                     f'Для перехода обратно в меню фильтров нажмите "В меню поиска"'
                                                     f'',
                         keyboard=keyboard2)

        if payload == 56:
            temp = 'for_56'
            send_message(peer_id=peer_id_in, message='Теперь нужно выбрать жанр:\n'
                                                     f'{category_list}',
                         keyboard=keyboard)

        # Если ответ по жанру есть в списке - присваиваем жанр. Temp - различие для клавиатуры
        elif payload in [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18] and temp == 'for_56':
            second_genre_id = payload - 6
            send_message(peer_id=peer_id_in,
                         message=f'Второй жанр был успешно выбран - {list_of_genres[second_genre_id]["Genre name"]}.\n\n'
                                 'При выборе жанра можно несколько раз нажимать на указанные'
                                 ' кнопки с цифрами, если Вы решили изменить свое решение',
                         keyboard=keyboard2)

        vk.messages.markAsRead(peer_id=peer_id_in)

