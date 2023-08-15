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
        # token = 'vk1.a.gt5yl2xL16U5GpKb-A84V70zi2REmMn-a4xIh0d9UQ2Eoco60t-7U5bJ2kPRqu_fme9PvKgIAr2Q8Wi9k3CGdVsJv0Qq0wY4SHr_nHGMCQZj4uN5zibCfr4AWBwmpBasgGyWXwnkkXn5sXWygnkudMCgI26ZnrYKNvxUQ-HGYqG-A_U2KCANG0WQ57QupVeOJ1uyQKIBp597RuzGiWKG0A'
        # url_method = 'https://api.vk.com/method'
        params = {
            'access_token': self.token,
            'owner_id': self.id, 
            'album_id': 'profile',
            'extended': '1',
            'photo_size': '1',
            'v': 5.131
        }
        response = requests.get(f'{self.url_method}/photos.get?{urlencode(params)}').json()
        return response
    
    def max_size_photo(self):
        name_size = {}
        try:
            for i in [n for n in self.photo_get()["response"]['items']]:
                if i['likes']['count'] in name_size.keys():
                    name_size[i['date']] = (list(reversed(i['sizes']))[0])
                else:
                    name_size[i['likes']['count']] = (list(reversed(i['sizes']))[0])
            json_dump = [{'file_name': f"{i}.jpg", 'size': o['type']} for i, o in name_size.items()]
            json_dumps = json.dumps(json_dump, indent=4)
            with open('data.json', 'w') as file:
                file.write(json_dumps)
        except KeyError:
            return f'Такого пользователя с ID {self.id} не существует.'
        return name_size

class YaDiskAPI(VkAPI):

    url_ya = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, poligon_ya, id):
        super().__init__(id)
        self.poligon_ya = poligon_ya

    def create_file(self):
        # url_ya = 'https://cloud-api.yandex.net/v1/disk/resources'
        params_ya = {'path': "Your photo's"}
        headers_ya = {'Authorization': f'OAuth {self.poligon_ya}'}
        response = requests.put(f"{self.url_ya}?{urlencode(params_ya)}", headers=headers_ya).json()
        return response
    
    def upload_files(self):
        self.create_file()
        headers_ya = {'Authorization': f'OAuth {self.poligon_ya}'}
        for likes, url in tqdm(self.max_size_photo().items(), desc='Загружаем фотографии', ncols=80, colour='#00FF00'):
            params_ya = {'url': url['url'], 'path': f"Your photo's/{likes}.jpg"}
            requests.post(f"{self.url_ya}/upload?{urlencode(params_ya)}", headers=headers_ya).json()
            time.sleep(0.5)
        return 'Загрузка завершена.'
    
    

people_1 = YaDiskAPI(poligon_ya=input('Введите токен из полигона яндекс диска: '), id=input('Введите id вашей страницы в Вконтакте: '))
print(people_1.upload_files())
