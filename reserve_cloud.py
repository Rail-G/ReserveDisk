from urllib.parse import urlencode
import requests
import json
import time
from tqdm import tqdm

class VkAPI():

    token = 'vk1.a.gt5yl2xL16U5GpKb-A84V70zi2REmMn-a4xIh0d9UQ2Eoco60t-7U5bJ2kPRqu_fme9PvKgIAr2Q8Wi9k3CGdVsJv0Qq0wY4SHr_nHGMCQZj4uN5zibCfr4AWBwmpBasgGyWXwnkkXn5sXWygnkudMCgI26ZnrYKNvxUQ-HGYqG-A_U2KCANG0WQ57QupVeOJ1uyQKIBp597RuzGiWKG0A'
    url_method = 'https://api.vk.com/method'

    def __init__(self, id):
        self.id = id

    def photo_get(self):
        """
        Получение доступа к фотографиям пользователя ВК.
        """

        params = {
            'access_token': self.token,
            'owner_id': self.id, 
            'album_id': 'profile',
            'extended': '1',
            'photo_size': '1',
            'count': '5',
            'v': 5.131
        }
        try:
            response = requests.get(f'{self.url_method}/photos.get?{urlencode(params)}').json()
            return response["response"]['items']
        except KeyError:
            return f'Такого пользователя с ID {self.id} не существует.'
    
    def max_size_photo(self):
        """
        Нахождения максимального размера фотография и записаь его в json файл.
        """
        responses = self.photo_get()
        data = []
        photo_name = []

        for i in responses:
            max_size = i['sizes'][-1]
            name = i['likes']['count']
            if name in photo_name:
                name = f"{i['likes']['count']}_{i['date']}"
            photo_name.append(name)
            url = max_size['url']
            type = max_size['type']
            data.append({'name': name, 'url': url, 'type': type})
        json_dump = [{'file_name': f"{i['name']}.jpg", 'size': i['type']} for i in data]
        with open('data.json', 'w') as file:
            json.dump(json_dump, file, indent=4)
        return data

class YaDiskAPI(VkAPI):

    url_ya = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, poligon_ya, id):
        super().__init__(id)
        self.poligon_ya = poligon_ya

    def create_file(self):
        """
        Создание папки на яндекс диске.
        """
        params_ya = {'path': "Your photo's"}
        headers_ya = {'Authorization': f'OAuth {self.poligon_ya}'}
        response = requests.put(f"{self.url_ya}?{urlencode(params_ya)}", headers=headers_ya).json()
        return response
    
    def upload_files(self):
        """
        Загрузка фотографии на созданную папку.
        """
        self.create_file()
        headers_ya = {'Authorization': f'OAuth {self.poligon_ya}'}
        for i in tqdm(self.max_size_photo(), desc='Загружаем фотографии', ncols=80, colour='#00FF00'):
            params_ya = {'url': i['url'], 'path': f"Your photo's/{i['name']}.jpg"}
            requests.post(f"{self.url_ya}/upload?{urlencode(params_ya)}", headers=headers_ya).json()
            time.sleep(0.3)
        return 'Загрузка завершена.'
    
    

people_1 = YaDiskAPI(poligon_ya=input('Введите токен из полигона яндекс диска: '), id=input('Введите id вашей страницы в Вконтакте: '))
print(people_1.upload_files())

