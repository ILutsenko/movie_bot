list_of_genres = {
        1: {'Genre name': 'Комедии',
            'code': 'comedy'},
        2: {'Genre name': 'Научная фантастика',
            'code': 'sci-fi'},
        3: {'Genre name': 'Ужасы',
            'code': 'horror'},
        4: {'Genre name': 'Романтика',
            'code': 'romance'},
        5: {'Genre name': 'Боевики',
            'code': 'action'},
        6: {'Genre name': 'Триллер',
            'code': 'thriller'},
        7: {'Genre name': 'Драмы',
            'code': 'drama'},
        8: {'Genre name': 'Детективы',
            'code': 'mystery'},
        9: {'Genre name': 'Документальные детективы',
            'code': 'crime'},
        10: {'Genre name': 'Мультфильмы',
             'code': 'animation'},
        11: {'Genre name': 'Приключения',
             'code': 'adventure'},
        12: {'Genre name': 'Фантастика',
             'code': 'fantasy'},
        13: {'Genre name': 'Комедийные драмы',
             'code': 'comedy,romance'},
        14: {'Genre name': 'Комедийные боевики',
             'code': 'action,comedy'},
        15: {'Genre name': 'Семейный',
             'code': 'family'},
        16: {'Genre name': 'Спорт',
             'code': 'sport'},
        17: {'Genre name': 'Короткометражки',
             'code': 'short'},
        18: {'Genre name': 'Военные',
             'code': 'war'},
        19: {'Genre name': 'Игровые шоу',
             'code': 'game_show'},
        20: {'Genre name': 'Мюзиклы',
             'code': 'musical'},
        21: {'Genre name': 'Биография',
             'code': 'biography'},
        22: {'Genre name': 'Noir',
             'code': 'film-noir'},
        23: {'Genre name': 'Вестерны',
             'code': 'western'},
        24: {'Genre name': 'Исторические',
             'code': 'history'},
        25: {'Genre name': 'Музыкальные',
             'code': 'music'},
        26: {'Genre name': 'Документальные',
             'code': 'documentary'},
        27: {'Genre name': 'Реалити шоу',
             'code': 'reality_tv'},
}

category_list = '\n'
for genre in list_of_genres:
    name = list_of_genres[genre]['Genre name']
    category_list += f"{genre}: {name}\n"
    if genre == 12:
        break
