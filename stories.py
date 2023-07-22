import requests
import os
from pathlib import Path
from utils.get_urls import Urls
from utils.constants import Tokens, Group_ID, User_Tokens, BASE_URL
from utils.common import get_data_from_yaml


class Stories:
    """
    Класс для работы с историями
    """
    def __init__(self, config):
        self.ver_api = config.general.ver_api
        self.group_name = config.general.group_name
        self.path_story = Path(f'stories/{self.group_name}')
        self.token = self.initialize(config.general.group_name)
        self.url = Urls(self.group_name, self.token, self.ver_api)
        self.group_id = Group_ID[self.group_name]
        self.__check_story(self.group_id)
        self.get_last_post()
        self.publish_story()

    def initialize(self, group_name):
        """Получение токена группы по её названию для дальнейшей работы с историями"""
        if group_name not in Tokens:
            raise OSError(f'Проверьте group_name в конфиге. group_name = {group_name}')
        if not os.path.exists('stories'):
            os.mkdir('stories')
        if not os.path.exists(self.path_story):
            os.mkdir(self.path_story)
        return Tokens[group_name]
    
    def __check_story(self, owner_id):
        """Метод для определения, постилась ли сегодня история или нет"""
        url = self.url.url_get_stories(self.token, owner_id)
        req = requests.get(url).json()['response']['items']
        if not req:
            return 1
        if len(req[0]['stories']) < 2:
            return 1
        else:
            raise OSError('Количество историй больше двух')
        
    def get_last_post(self):
        """Метод для получения последнего поста и ссылки к нему, для привязки к истории"""
        token = User_Tokens['Тимер']
        last_posts = requests.get(f'{BASE_URL}wall.get?access_token={token}&owner_id=-{self.group_id}&count=2&v={self.ver_api}').json()['response']
        if 'error' in last_posts:
            raise OSError('error in response in get_last_posts')
        
        for post in last_posts['items']:
            if post['marked_as_ads']:
                continue
            self.id_post = post['id']
            attach = post['attachments'][0]['photo']['sizes'][-1]['url']
            content = requests.get(attach).content
            self.story_path = self.path_story / 'story.jpg'
            with open(self.story_path, 'wb') as file:
                file.write(content)
            return 1
        return 0

    def publish_story(self):
        """Метод постинга истории"""
        file = {}
        url = self.url.url_store_server(token = self.token, link_url = f'https://vk.com/wall-{self.group_id}_{self.id_post}')
        upload_url = requests.get(url).json()['response']['upload_url']
        with open(self.story_path, 'rb') as image:
            file['photo'] = image
            story = requests.post(upload_url, files = file).json()['response']['upload_result']
        url = self.url.url_save_store(token = self.token, upload_result = story)
        result = requests.get(url).json()
        assert result['response']['count'] == 1, 'Неизвестная ошибка, нужно подебажить'
    
    def __preproccess(self, image):
        """
        TODO:Сделать препроцессинг для картинок в истории. Соотношение сторон 9:16, разрешение 720х1280.
        Добавить наложение текста
        1. Картинка подходит, просто обрезается
        2. Не хватает ширины
        3. Не хватает высоты
        """
        pass

if __name__ == '__main__':
    config = get_data_from_yaml('configs/config.yaml')
    story = Stories(config)
