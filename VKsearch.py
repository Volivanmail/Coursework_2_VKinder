from pprint import pprint
import requests

class vk_user_search:

    def __init__(self, token_VK, city, sex, status, age_from, age_to):
        self.token_VK = token_VK
        self.city = city
        self.sex = sex
        self.status = status
        self.age_from = age_from
        self.age_to = age_to

    def token_vk(self):
        with open(self.token_VK, encoding='utf-8') as f:
            token_vk = f.read().strip()
            return token_vk

    def VK_search(self):
        URL = 'https://api.vk.com/method/users.search'
        token = self.token_vk()
        params = {
            'access_token': token,
            'v': '5.131',
            'fields': 'bdate, city',
            'status': self.status,
            'count': '3',
            'city': self.city,
            'sex': self.sex,
            'age_from': self.age_from,
            'age_to': self.age_to
            }
        res_user = requests.get(URL, params).json()['response']['items']
        for user in res_user:
            user_id = user['id']
            print(user_id)
            URL = 'https://api.vk.com/method/photos.get'
            token = self.token_vk()
            params = {
                'access_token': token,
                'v': '5.131',
                'owner_id': user_id,
                'album_id': 'profile',
                'extended': '1',
                'count': '1000'
            }
            res_photo = requests.get(URL, params).json()['response']['items']
            return res_photo
            # photo_album = []
            # likes_list = []
            # for photo in res_photo:
            #     photo_dict = {}
            #     if photo['likes']['count'] not in likes_list:
            #         name = str(photo['likes']['count'])
            #         likes_list.append(photo['likes']['count'])
            #     else:
            #         name = str(photo['likes']['count']) + str(photo['date'])
            #     photo_dict['file_name'] = name
            #     for i in photo['sizes']:
            #         s_max = 0
            #         s = int(i['height']) * int(i['width'])
            #         if s > s_max:
            #             photo_dict['sizes'] = i['type']
            #             photo_dict['link'] = i['url']
            #             s_max = s
            #     photo_album.append(photo_dict)
            # pprint(photo_album)
            # return photo_album



# URL = 'https://api.vk.com/method/photos.get'
#             token = self.token_vk()
#             params = {
#                 'access_token': token,
#                 'v': '5.131',
#                 'owner_id': user_id,
#                 'album_id': 'profile',
#                 'extended': '1',
#                 'count': '1000'
#             }
#             res_photo = requests.get(URL, params).json()['response']['items']
#             pprint(res_photo)
#             photo_album = []
#             likes_list = []
#             for photo in res_photo:
#                 photo_dict = {}
#                 if photo['likes']['count'] not in likes_list:
#                     name = str(photo['likes']['count'])
#                     likes_list.append(photo['likes']['count'])
#                 else:
#                     name = str(photo['likes']['count']) + str(photo['date'])
#                 photo_dict['file_name'] = name
#                 for i in photo['sizes']:
#                     s_max = 0
#                     s = int(i['height']) * int(i['width'])
#                     if s > s_max:
#                         photo_dict['sizes'] = i['type']
#                         photo_dict['link'] = i['url']
#                         s_max = s
#                 photo_album.append(photo_dict)
#             pprint(photo_album)
#             return photo_album

