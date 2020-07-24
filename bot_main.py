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
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Начальный год', VkKeyboardColor.PRIMARY, payload=23)
        keyboard.add_button('Конечный год', VkKeyboardColor.PRIMARY, payload=24)
        keyboard.add_line()
        keyboard.add_button('Ничего не менять', VkKeyboardColor.PRIMARY, payload=3)
        keyboard.add_line()
        keyboard.add_button('Я хочу начать сначала', VkKeyboardColor.DEFAULT, payload=0)
        return keyboard.get_keyboard()
    elif payload == 20:
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Мин. рейтинг', VkKeyboardColor.PRIMARY, payload=25)
        keyboard.add_button('Макс. рейтинг', VkKeyboardColor.PRIMARY, payload=26)
        keyboard.add_line()
        keyboard.add_button('Ничего не менять', VkKeyboardColor.PRIMARY, payload=3)
        keyboard.add_line()
        keyboard.add_button('Я хочу начать сначала', VkKeyboardColor.DEFAULT, payload=0)
        return keyboard.get_keyboard()

    elif payload == 21:
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
        keyboard.add_button('Вернуться к поиску', VkKeyboardColor.PRIMARY, payload=3)
        keyboard.add_line()
        keyboard.add_button('Я хочу начать сначала', VkKeyboardColor.DEFAULT, payload=0)
        return keyboard.get_keyboard()

    if payload == 25 or payload == 26:
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
        keyboard.add_button('Ничего не менять', VkKeyboardColor.DEFAULT, payload=3)
        keyboard.add_line()
        keyboard.add_button('Я хочу начать сначала', VkKeyboardColor.DEFAULT, payload=0)
        return keyboard.get_keyboard()

    if payload in [39, 40, 41, 42, 43, 44, 45, 46, 47, 48]:
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Вернуться к  поиску', VkKeyboardColor.PRIMARY, payload=20)
        keyboard.add_line()
        keyboard.add_button('Вернуться в начало', VkKeyboardColor.PRIMARY, payload=20)
        return keyboard.get_keyboard()


def start_menu():
    if payload == None or payload == 0:
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Я уже знаю что посмотреть', payload=1, color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Я хочу выбрать рандомно', VkKeyboardColor.PRIMARY, payload=2)
        keyboard.add_line()
        keyboard.add_button('Продвинутый поиск', VkKeyboardColor.PRIMARY, payload=3)
        keyboard.add_line()
        keyboard.add_button('Топ 100 фильмов\сериалов по жанрам', VkKeyboardColor.PRIMARY, payload=4)
        return keyboard.get_keyboard()

    if payload == 1:
        pass

    elif payload == 2:
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Фильм', VkKeyboardColor.PRIMARY, payload=5)
        keyboard.add_button('Сериал', VkKeyboardColor.PRIMARY, payload=6)
        keyboard.add_line()
        keyboard.add_button('Я хочу начать сначала', VkKeyboardColor.PRIMARY, payload=0)
        return keyboard.get_keyboard()

    elif payload == 3:
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Выбрать год', VkKeyboardColor.PRIMARY, payload=19)
        keyboard.add_line()
        keyboard.add_button('Выбрать рейтинг', VkKeyboardColor.PRIMARY, payload=20)
        keyboard.add_line()
        keyboard.add_button('Выбрать жанр', VkKeyboardColor.PRIMARY, payload=21)
        keyboard.add_line()
        keyboard.add_button('Я хочу начать сначала', VkKeyboardColor.PRIMARY, payload=0)
        return keyboard.get_keyboard()

    elif payload == 4:
        pass

    if payload == 5 or payload == 6 or payload == 21:
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
            keyboard.add_button('Я хочу начать сначала', VkKeyboardColor.DEFAULT, payload=0)
            return keyboard.get_keyboard()
        elif payload == 6:
            keyboard.add_line()
            keyboard.add_button('Переключить на фильмы', VkKeyboardColor.DEFAULT, payload=5)
            keyboard.add_line()
            keyboard.add_button('Я хочу начать сначала', VkKeyboardColor.DEFAULT, payload=0)
            return keyboard.get_keyboard()
        else:
            return keyboard.get_keyboard()


VK_API_VERSION = '5.120'
GROUP_ID = 197300375
VK_API_ACCESS_TOKEN = '50b21743f85bf752ccb5a0f29a1009e0f7bac25bbd6e0ef9211acb4fdb33bb1d5f11099497f14409c561c'


vk_session = vk_api.VkApi(token=VK_API_ACCESS_TOKEN)
vk = vk_session.get_api()

# Первый запрос к LongPoll: получаем server и key
longpoll = VkBotLongPoll(vk_session, 197300375)
film_or_serial = 0
films_list = []
temp = 0
min_rating = 6
max_rating = 10
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
        if payload == None:
            send_message(peer_id=peer_id_in, message='Мы в главном меню', keyboard=keyboard)
        elif payload == 2:
            send_message(peer_id=peer_id_in, message='Для рандомного выбора нужно выбрать категорию:', keyboard=keyboard)
        elif payload == 3:
            send_message(peer_id=peer_id_in, message='В меню продвинутого поиска: ',
                         keyboard=keyboard)

        elif payload == 5 or payload == 6:
            temp = 'basic'
            send_message(peer_id=peer_id_in, message='Теперь нужно выбрать жанр:\n'
                                                     f'{category_list}',
                         keyboard=keyboard)
            film_or_serial = payload
        if payload in [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18] and temp != 'for_21':
            genre_id = payload - 6
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

        keyboard2 = key_advanced()
        if payload == 19:
            send_message(peer_id=peer_id_in, message='Автоматически минимальный год выставлен на 2000, а '
                                                     'максимальный - на 2020. Получается такой формат: '
                                                     '2010 - 2020. Если будем изменять - нажмите на соответствующую'
                                                     'кнопку. Если нет, то нажмите "ничего не менять". ',
                         keyboard=keyboard2)

        elif payload == 20:
            send_message(peer_id=peer_id_in, message='Автоматически минимальный рейтинг выставлен на 6, а '
                                                     'максимальный - на 10. Получается такой формат: '
                                                     '6 - 10. Если будем изменять - нажмите на соответствующую'
                                                     'кнопку. Если нет, то нажмите "ничего не менять" ',
                         keyboard=keyboard2)

        elif payload == 21:
            temp = 'for_21'
            send_message(peer_id=peer_id_in, message='Теперь нужно выбрать жанр:\n'
                                                     f'{category_list}',
                         keyboard=keyboard)
        elif payload in [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18] and temp == 'for_21':
            genre_id = payload - 6
            send_message(peer_id=peer_id_in,
                         message=f'Жанр был успешно выбран - {list_of_genres[genre_id]["Genre name"]}',
                         keyboard=keyboard2)

        elif payload == 25 or payload == 26:
            if payload == 25:
                temp = 'min'
                send_message(peer_id=peer_id_in, message='Автоматически минимальный рейтинг выставлен на 6, но это можно '
                                                         'изменить здесь',
                             keyboard=keyboard2)
            elif payload == 26:
                temp = 'max'
                send_message(peer_id=peer_id_in, message='Автоматически максимальный рейтинг выставлен на 10, но это можно '
                                                         'изменить здесь',
                             keyboard=keyboard2)

        if payload in [39, 40, 41, 42, 43, 44, 45, 46, 47, 48]:
            if temp == 'min':
                min_rating = payload - 38
                send_message(peer_id=peer_id_in,
                             message='минимальный рейтинг успешно изменен',
                             keyboard=keyboard2)
            elif temp == 'max':
                max_rating = payload - 38
                send_message(peer_id=peer_id_in,
                             message='максимальный рейтинг успешно изменен',
                             keyboard=keyboard2)
        print(f'минимальный рейтинг - {min_rating}')
        print(f'Максммальный рейтинг - {max_rating}')
        print(f'Payload - {payload}')
        try:
            print(f'Это жанр - {genre_id}')
        except:
            pass
        print()

        vk.messages.markAsRead(peer_id=peer_id_in)

