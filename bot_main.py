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
        keyboard.add_line()
        keyboard.add_button('Я хочу начать сначала', VkKeyboardColor.PRIMARY, payload=0)
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
        pass

    elif payload == 4:
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('1', VkKeyboardColor.PRIMARY, payload=19)
        keyboard.add_button('2', VkKeyboardColor.PRIMARY, payload=20)
        keyboard.add_button('3', VkKeyboardColor.PRIMARY, payload=21)
        keyboard.add_button('4', VkKeyboardColor.PRIMARY, payload=22)
        keyboard.add_line()
        keyboard.add_button('5', VkKeyboardColor.PRIMARY, payload=23)
        keyboard.add_button('6', VkKeyboardColor.PRIMARY, payload=24)
        keyboard.add_button('7', VkKeyboardColor.PRIMARY, payload=25)
        keyboard.add_button('8', VkKeyboardColor.PRIMARY, payload=26)
        keyboard.add_line()
        keyboard.add_button('9', VkKeyboardColor.PRIMARY, payload=27)
        keyboard.add_button('10', VkKeyboardColor.PRIMARY, payload=28)
        keyboard.add_button('11', VkKeyboardColor.PRIMARY, payload=29)
        keyboard.add_button('12', VkKeyboardColor.PRIMARY, payload=30)
        keyboard.add_line()
        return keyboard.get_keyboard()

    if payload == 5 or payload == 6:
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
        keyboard.add_line()
        if payload == 5:
            keyboard.add_button('Переключить на сериалы', VkKeyboardColor.DEFAULT, payload=6)
            keyboard.add_line()
            keyboard.add_button('Я хочу начать сначала', VkKeyboardColor.DEFAULT, payload=0)
            return keyboard.get_keyboard()
        elif payload == 6:
            keyboard.add_button('Переключить на фильмы', VkKeyboardColor.DEFAULT, payload=5)
            keyboard.add_line()
            keyboard.add_button('Я хочу начать сначала', VkKeyboardColor.DEFAULT, payload=0)
            return keyboard.get_keyboard()


VK_API_VERSION = '5.120'
GROUP_ID = 197300375
VK_API_ACCESS_TOKEN = '50b21743f85bf752ccb5a0f29a1009e0f7bac25bbd6e0ef9211acb4fdb33bb1d5f11099497f14409c561c'


vk_session = vk_api.VkApi(token=VK_API_ACCESS_TOKEN)
vk = vk_session.get_api()

# Первый запрос к LongPoll: получаем server и key
longpoll = VkBotLongPoll(vk_session, 197300375)
film_or_serial = 0
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
            send_message(peer_id=peer_id_in, message='Продвинутый поиск: ',
                         keyboard=keyboard)
        elif payload == 4:
            send_message(peer_id=peer_id_in, message='Теперь нужно выбрать жанр:\n'
                                                     f'{category_list}',
                         keyboard=keyboard)
        if payload in [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]:
            genre_id = payload - 18
            db = get_connection()
            cursor = db.cursor()
            selector_for_genre = ('SELECT * FROM genre_movie WHERE genre_id = %s')
            cursor.execute(selector_for_genre, (genre_id,))
            films_for_categories = [x[1] for x in cursor.fetchall()]
            best_films = films_for_categories[:101]
            for film_gen in best_films:
                selector = ('SELECT * FROM movie WHERE premier > 2001 and rating > 6 and type_id = 0 and duration > 0 and votes > 25000 and id = %s')
                film = random_film[0]
                cursor.execute(selector, (film,))
                checker = cursor.fetchall()


        elif payload == 5 or payload == 6:
            send_message(peer_id=peer_id_in, message='Теперь нужно выбрать жанр:\n'
                                                     f'{category_list}',
                         keyboard=keyboard)
            film_or_serial = payload
        if payload in [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]:
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

        vk.messages.markAsRead(peer_id=peer_id_in)

