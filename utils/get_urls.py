import requests
from .constants import BASE_URL

class Urls:
    """
        Класс для генерации урлов в зависимости от метода
    """
    def __init__(self, group_name, token, ver_api):
        self.group_name = group_name
        self.token = token
        self.ver_api = ver_api

    def url_get_group_id(self):
        """
        Генерация url для получения id группы по ссылке-имени
        """
        url = f'{BASE_URL}wall.get?domain={self.group_name}' \
                f'&count=100&offset=1&access_token={self.token}&v={self.ver_api}'
        return url

    def url_get_server(self, group_id):
        """
        Генерация url для поиска сервера
        """
        url = f'{BASE_URL}photos.getWallUploadServer?' \
            f'group_id={group_id}&access_token={self.token}&v={self.ver_api}'
        return url

    def url_save_photo(self, group_id, photo, server, hash):
        """
        Генерация url для предварительной загрузки фото на сервер
        """
        url = f'{BASE_URL}photos.saveWallPhoto?access_token={self.token}' \
            f'&group_id={group_id}&photo={photo}&server={server}&hash={hash}&v={self.ver_api}'
        return url

    def url_publish_post(self, group_id, photos, text, date=None):
        """
        Генерация url для публикации поста
        """
        if date == None:
            url = f'{BASE_URL}wall.post?owner_id=-{group_id}' \
                f'&attachments={photos}&message={text}&from_group=1&access_token={self.token}&v={self.ver_api}'
        else:
            url = f'{BASE_URL}wall.post?owner_id=-{group_id}' \
                f'&attachments={photos}&message={text}&publish_date={date}&from_group=1&access_token={self.token}&v={self.ver_api}'
        return url
    
    def url_get_stories(self, token, owner_id):
        return f'{BASE_URL}stories.get?access_token={token}&owner_id=-{owner_id}&v={self.ver_api}'
    
    def url_store_server(self, token, link_url):
        """
        Генерация url`а для загрузки фото-стори на сервер
        """
        return f'{BASE_URL}stories.getPhotoUploadServer?access_token={token}&link_text=learn_more&link_url={link_url}&add_to_news=1&v={self.ver_api}'

    def url_save_store(self, token, upload_result):
        """
        Сохранение в профиль/группу загруженной истории
        """
        return f'https://api.vk.com/method/stories.save?access_token={token}&upload_results={upload_result}&v={self.ver_api}'