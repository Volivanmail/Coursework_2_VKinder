import requests
from random import randint


def random():
    x = randint(0,20)
    return x


class vk_user_search:

    def __init__(self, token_VK, city, sex, status, age_from, age_to):
        self.token_VK = token_VK
        self.city = city
        self.sex = sex
        self.status = status
        self.age_from = age_from
        self.age_to = age_to
        self.URL = 'https://api.vk.com/method/'

    def VK_search(self):
        URL = self.URL + 'users.search'
        token = self.token_VK
        params = {
            'access_token': token,
            'v': '5.131',
            'offset': random(),
            'status': self.status,
            'count': '1',
            'city': self.city,
            'sex': self.sex,
            'age_from': self.age_from,
            'age_to': self.age_to,
            'has_photo': '1'
            }
        try:
            user = requests.get(URL, params).json()['response']['items'][0]
            if user['is_closed'] == True:
                self.VK_search()
            else:
                return user
        except:
            self.VK_search()

    def VK_get_photo(self):
        try:
            user = self.VK_search()
            user_id = user['id']
            URL = self.URL + 'photos.get'
            token = self.token_VK
            params = {
                'access_token': token,
                'v': '5.131',
                'owner_id': user_id,
                'album_id': 'profile',
                'extended': '1',
                'count': '500'
            }
            res_photo = requests.get(URL, params).json()['response']
            if res_photo['count'] <=2:
                self.VK_get_photo()
            else:
                photo_album = []
                likes_list =[]
                for photo in res_photo['items']:
                    likes_list.append(photo['likes']['count'])
                likes_list.sort(reverse=True)
                likes_list = likes_list[:3]
                for photo in res_photo['items']:
                    photo_dict = {}
                    if photo['likes']['count'] in likes_list:
                        photo_dict['id'] = photo['id']
                        photo_dict['url'] = photo['sizes'][-1]['url']
                        photo_album.append(photo_dict)
                photo_album = photo_album[:3]
            return user_id, photo_album
        except KeyError:
            self.VK_get_photo()
        except TypeError:
            self.VK_get_photo()
        except UnboundLocalError:
            self.VK_get_photo()

