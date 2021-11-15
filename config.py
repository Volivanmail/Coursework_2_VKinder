DNS = 'postgresql://forvk:123vk@localhost:5432/bd_user_vk'


with open('D:\\Study_Pyton\\dip_par\\token_VK.txt', encoding='utf-8') as f:
    # для проверок что бы каждый раз токен не вводить
    token_VK = f.read().strip()

with open('D:\\Study_Pyton\\dip_par\\token_vk_vkpy.txt', encoding='utf-8') as f:
    # для проверок что бы каждый раз токен не вводить
    token_bot = f.read().strip()