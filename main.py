from random import randrange
from pprint import pprint
from datetime import date
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from VKsearch import vk_user_search

# token = input('Token: ')

token_VK = 'D:\\Study_Pyton\\dip_par\\token_VK.txt'

with open('D:\\Study_Pyton\\dip_par\\token_vk_vkpy.txt', encoding='utf-8') as f:
    # для проверок что бы каждый раз токен не вводить
    token = f.read().strip()


session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(session)


def write_msg(user_id, message, keyboard=None):
    post = {'user_id': user_id, 'message': message,
                                     'random_id': randrange(10 ** 7)}
    if keyboard is not None:
        post ['keyboard'] = keyboard.get_keyboard()

    session.method('messages.send', post)

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
        sex_name = 'женщину'
        sex_relation = 'не замужнюю'
    else:
        sex_search = 0
        sex_name = 'любого пола'
        sex_relation = 'не женат/не замужем'
    sex_user = [sex_search, sex_name, sex_relation]
    return sex_user

def status_relation (status):
    # пока не пригодилась
    dict_relation = {1: 'не женат/не замужем', 2: 'есть друг/есть подруга', 3: 'помолвлен/помолвлена',
                     4: 'женат/замужем', 5: 'всё сложно', 6: 'в активном поиске', 7: 'влюблён/влюблена',
                     8: 'в гражданском браке', 0: 'не указано'}
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

# user_base = {}

# def start():
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user_id = event.user_id
        user = user_info(user_id)
        user = user[0]
        sex_for_search = get_sex_for_search(user['sex'])
        age = get_age(user_id)
        city_search = user['city']['id']
        sex_search = sex_for_search[0]
        sex_name = sex_for_search[1]
        age_from_to_list = age_from_to(sex_search, age)
        if request.lower() == "привет":
            write_msg(user_id, f"Хай, {user['first_name']}")
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('Да', VkKeyboardColor.POSITIVE)
            keyboard.add_button('Нет', VkKeyboardColor.NEGATIVE)
            write_msg(user_id, f"Найдем тебе пару?", keyboard)
        elif request == "нет":
            write_msg(user_id, "Может быть в следующий раз! Пока((")
        elif request.lower() == "да":
            write_msg(user_id, f"ок")
            if user['city']['title']:
                write_msg(user_id, f" Ты из города {user['city']['title']}")
            if age:
                write_msg(user_id, f" Тебе {age} {age_spelling_check(age)}")
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Поиск', VkKeyboardColor.POSITIVE)
                keyboard.add_button('Поменять параметры', VkKeyboardColor.NEGATIVE)
                write_msg(user_id, f"Ищем в твоем городе, {sex_name} от {age_from_to_list[0]} до {age_from_to_list[1]}"
                                   f" и, осмелюсь предположить, {sex_for_search[2]} ))) по этим параметрам?",keyboard)
        elif request.lower() == "поиск":
                user_search = vk_user_search(token_VK, city_search, sex_search,
                                             '1', age_from_to_list[0], age_from_to_list[1])
                res = user_search.VK_search()
                for user in res:
                    write_msg(user_id, f"{user['sizes'][-1]['url']}")
        else:
            write_msg(user_id, "Ответ не понятен...")


# if __name__ == '__main__':
