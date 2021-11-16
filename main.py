from random import randrange
from time import sleep
from datetime import date
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from VKsearch import vk_user_search
from config import token_bot, token_VK
import requests
from bd.bdsearch import add_user, add_user_search, add_user_favourites, get_user_search

session = vk_api.VkApi(token=token_bot)
longpoll = VkLongPoll(session)


def write_msg(user_id, message,keyboard=None):
    post = {'user_id': user_id, 'message': message,
                                     'random_id': randrange(10 ** 7)}
    if keyboard is not None:
        post ['keyboard'] = keyboard.get_keyboard()

    session.method('messages.send', post)

def write_msg_photo(user_id, attachment):
    post = {'user_id': user_id, 'attachment': attachment, 'random_id': randrange(10 ** 7)}
    session.method('messages.send', post)

data_search = {}

def start():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            request = event.text.lower()
            user_id = event.user_id
            user = user_info(user_id)
            user = user[0]
            if request.lower() == "привет":
                write_msg(user_id, f"Хай, {user['first_name']}")
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Да', VkKeyboardColor.POSITIVE)
                keyboard.add_button('Нет', VkKeyboardColor.NEGATIVE)
                write_msg(user_id, f"Найдем тебе пару?", keyboard)
            elif request == "нет":
                write_msg(user_id, "Может быть в следующий раз?! Пока((")
            elif request.lower() == "да":
                write_msg(user_id, f"ок")
                sex_for_search = get_sex_for_search(user['sex'])
                age = get_age(user_id)
                sex_search = sex_for_search[0]
                sex_name = sex_for_search[1]
                age_from_to_list = age_from_to(sex_search, age)
                data_search['city'] = user['city']
                data_search['sex'] = sex_search
                data_search['status'] = '1'
                data_search['age_from'] = age_from_to_list[0]
                data_search['age_to'] = age_from_to_list[1]
                if user['city']['title']:
                    write_msg(user_id, f" Твой город {user['city']['title']}")
                if age:
                    write_msg(user_id, f" Тебе {age} {age_spelling_check(age)}")
                    sleep(1)
                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button('Поиск', VkKeyboardColor.POSITIVE)
                    keyboard.add_button('Поменять параметры', VkKeyboardColor.NEGATIVE)
                    write_msg(user_id, f"Ищем в твоем городе, {sex_name} от {age_from_to_list[0]}"
                                       f" до {age_from_to_list[1]} и, осмелюсь предположить, {sex_for_search[2]}"
                                       f"))) по этим параметрам?",keyboard)
            elif request.lower() == "поиск":
                search(user_id)
            elif request.lower() == "поменять параметры":
                write_msg(user_id, "ок")
                changing_parameters(user_id)
            else:
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Привет', VkKeyboardColor.POSITIVE)
                write_msg(user_id, "Ответ не понятен, введите правильную команду! Или начнем с начала?", keyboard)

def get_age(user_id):
    # функция вычисления количества полных лет
    user = session.method('users.get', {'user_id': user_id, 'fields': 'bdate'} )
    birth_date = user[0]['bdate'].split('.')
    today = date.today()
    age = today.year - int(birth_date[2])
    full_year_passed = (today.month, today.day) > (int(birth_date[1]), int(birth_date[0]))
    if not full_year_passed:
        age -= 1
    return age

def user_info(user_id):
    user = session.method('users.get', {'user_id': user_id, 'fields': 'relation, sex, city, bdate'})
    return user

def age_spelling_check(age):
    # функция определения правописания количества лет
    last_number = age % 10
    if 2 <= last_number <= 4 and age >14:
        res = 'года'
    elif last_number == 1 and age > 11:
        res = 'год'
    else:
        res = 'лет'
    return res

def get_sex_for_search(sex):
    # функция для перемены пола от исходного для поиска и некоторые переменные для текста сообщений
    sex_user = []
    if sex == 1:
        sex_search = 2
        sex_name = 'мужчину'
        sex_relation = 'не женатого'
    elif sex == 2:
        sex_search = 1
        sex_name = 'девушку'
        sex_relation = 'не замужнюю'
    else:
        sex_search = 0
        sex_name = 'любого пола'
        sex_relation = 'не женат/не замужем'
    sex_user = [sex_search, sex_name, sex_relation]
    return sex_user

def get_title_sex(sex):
    # функция для вывода имени пола в зависимости от переменной
    if sex == 2:
        sex_name = 'мужчину'
    elif sex == 1:
        sex_name = 'девушку'
    else:
        sex_name = 'любого пола'
    return sex_name

def status_relation(status):
    # функция вывода статуса
    dict_relation = {1: 'не женат/не замужем', 2: 'есть друг/есть подруга', 3: 'помолвлен/помолвлена',
                     4: 'женат/замужем', 5: 'всё сложно', 6: 'в активном поиске', 7: 'влюблён/влюблена',
                     8: 'в гражданском браке', 0: 'не указано'}
    status = int(status)
    relation = dict_relation[status]
    return relation

def age_from_to(sex_search, age):
    # функция для дельты возраста в поиске, мужчины предпочитают помоложе спутницу, женщины наооборот.
    if sex_search == 2:
        age_from = age
        age_to = age + 3
    elif sex_search == 1:
        age_from = age - 5
        age_to = age
    else:
        age_from = age - 1
        age_to = age + 1
    age_from_to_list = [age_from, age_to]
    return age_from_to_list

def search(user_id):
    user_search = vk_user_search(token_VK, data_search['city']['id'], data_search['sex'], data_search['status'],
                                 data_search['age_from'], data_search['age_to'])
    res = user_search.VK_get_photo()
    try:
        id_user_vk = res[0]
        id_user_vk_list = get_user_search(user_id)
        if id_user_vk in id_user_vk_list:
            search(user_id)
        add_user(user_id)
        add_user_search(id_user_vk, user_id)
        x=1
        for photo in res[x]:
            write_msg_photo(user_id, 'photo' + str(id_user_vk) + '_' + str(photo['id']))
            x+=1
        write_msg(user_id, f"https://vk.com/id{res[0]}")
    except TypeError:
        search(user_id)
    action_with_the_result(id_user_vk, user_id)

def action_with_the_result(id_user_vk, user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Поиск', VkKeyboardColor.POSITIVE)
    keyboard.add_button('Вернуться к смене параметров', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Добавить в избранное', VkKeyboardColor.POSITIVE)
    keyboard.add_button('Добавить в черный список', VkKeyboardColor.NEGATIVE)
    write_msg(user_id, f"Ну как?", keyboard)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            request = event.text.lower()
            user_id = event.user_id
            if request.lower() == "поиск":
                search(user_id)
            elif request.lower() == "вернуться к смене параметров":
                changing_parameters(user_id)
            elif request.lower() == "добавить в избранное":
                add_user_favourites(user_id, True, id_user_vk)
            elif request.lower() == "добавить в черный список":
                add_user_favourites(user_id, False, id_user_vk)
            else:
                write_msg(user_id, "Ответ не понятен")
            action_with_the_result(id_user_vk, user_id)

def changing_parameters(user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Город')
    keyboard.add_button('Семейное положение')
    keyboard.add_line()
    keyboard.add_button('Пол')
    keyboard.add_button('Возрастной диапозон')
    keyboard.add_line()
    keyboard.add_button('Посмотреть параметры поиска', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Поиск', VkKeyboardColor.POSITIVE)
    write_msg(user_id, f"Что меняем? Или поиск?", keyboard)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            request = event.text.lower()
            user_id = event.user_id
            if request.lower() == "город":
                write_msg(user_id, f"Введите название города полностю для избежания неточностей")
                change_sity()
            elif request.lower() == "поиск":
                search(user_id)
            elif request.lower() == "посмотреть параметры поиска":
                write_msg(user_id, f"Ищем  {get_title_sex(data_search['sex'])} от {data_search['age_from']}"
                                   f" до {data_search['age_to']} , {status_relation(data_search['status'])}"
                                   f" в городе {data_search['city']['title']}?")
                changing_parameters(user_id)
            elif request.lower() == "пол":
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('м',VkKeyboardColor.PRIMARY)
                keyboard.add_button('ж', VkKeyboardColor.PRIMARY)
                keyboard.add_line()
                keyboard.add_button('без разницы, мне для дружбы, а не для...', VkKeyboardColor.POSITIVE)
                write_msg(user_id,f'Выберай!!!', keyboard)
                change_sex()
            elif request.lower() == "семейное положение":
                write_msg(user_id, f"Введите цифру соответствующую желаемому статусу"
                                   f" 1 - не женат/не замужем" 
                                   f" 2 - есть друг/есть подруга"
                                   f" 3 - помолвлен/помолвлена"
                                   f" 4 - женат/замужем"
                                   f" 5 - всё сложно"
                                   f" 6 - в активном поиске"
                                   f" 7 - влюблён/влюблена"
                                   f" 8 - в гражданском браке"
                                   f" 0 - не указано")
                change_status()
            elif request.lower() == "возрастной диапозон":
                write_msg(user_id, f"Введите возрастной диапозон в формате: 16-90")
                change_age_search()
            elif request.lower() == "вернуться к смене параметров":
                changing_parameters(user_id)
            else:
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('вернуться к смене параметров', VkKeyboardColor.POSITIVE)
                write_msg(user_id, "Ответ не понятен, введите правильную команду! "
                                   "Или вернемся к смене параметров?", keyboard)

def change_sity():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            sity_title = event.text.capitalize()
            request = event.text.lower()
            if request.lower() == "вернуться к смене параметров":
                changing_parameters(user_id)
            else:
                try:
                    URL = 'https://api.vk.com/method/database.getCities'
                    token = token_VK
                    params = {'access_token': token, 'v': '5.131', 'country_id': '1', 'q': sity_title, 'count': '1'}
                    res_user = requests.get(URL, params).json()['response']['items']
                    data_search['city'] = res_user[0]
                    changing_parameters(user_id)
                except IndexError:
                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button('вернуться к смене параметров', VkKeyboardColor.POSITIVE)
                    write_msg(user_id, f"город введен не верно", keyboard)

def change_sex():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            request = event.text.lower()
            user_id = event.user_id
            if request.lower() == "м":
                data_search['sex'] = 2
            elif request.lower() == "ж":
                data_search['sex'] = 1
            else:
                data_search['sex'] = 0
            changing_parameters(user_id)

def change_status():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            request = event.text.lower()
            if request.lower() == "вернуться к смене параметров":
                changing_parameters(user_id)
            else:
                try:
                    if int(request) in range(10):
                        data_search['status'] = int(request)
                        changing_parameters(user_id)
                    else:
                        keyboard = VkKeyboard(one_time=True)
                        keyboard.add_button('вернуться к смене параметров', VkKeyboardColor.POSITIVE)
                        write_msg(user_id, "Ответ не понятен, введите правильные данные! Или начнем с начала?",
                                  keyboard)
                except ValueError:
                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button('вернуться к смене параметров', VkKeyboardColor.POSITIVE)
                    write_msg(user_id, "Ответ не понятен, введите правильные данные! Или начнем с начала?", keyboard)

def change_age_search():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            request = event.text.lower()
            if request.lower() == "вернуться к смене параметров":
                changing_parameters(user_id)
            else:
                request = request.split('-', 1)
                try:
                    if 0 < int(request[0]) <= int(request[1]) and int(request[1]) <= 120:
                        data_search['age_from'] = int(request[0])
                        data_search['age_to'] = int(request[1])
                        changing_parameters(user_id)
                    elif int(request[1]) > 120:
                        keyboard = VkKeyboard(one_time=True)
                        keyboard.add_button('вернуться к смене параметров', VkKeyboardColor.POSITIVE)
                        write_msg(user_id, "Столько не живут, введите адекватные данные, думаю до 120 достаточно!"
                                           " Или начнем с начала?",
                                  keyboard)
                    else:
                        keyboard = VkKeyboard(one_time=True)
                        keyboard.add_button('вернуться к смене параметров', VkKeyboardColor.POSITIVE)
                        write_msg(user_id, "Ответ не понятен, введите правильные данные! Или начнем с начала?",
                                  keyboard)
                except ValueError:
                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button('вернуться к смене параметров', VkKeyboardColor.POSITIVE)
                    write_msg(user_id, "Ответ не понятен, введите правильные данные! Или начнем с начала?", keyboard)

if __name__ == '__main__':
    start()
