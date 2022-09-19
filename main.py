import json
import requests
from auth_data import token
import os
import wotemark_add

def get_wall_posts(group_name, offset, owner_id=None):
    if owner_id == None:
        url = f'https://api.vk.com/method/wall.get?domain={group_name}&count=100&offset={offset}&access_token={token}&v=5.131'
    else:
        url = f'https://api.vk.com/method/wall.get?owner_id=-{owner_id}&count=100&offset={offset}&access_token={token}&v=5.131'
    req = requests.get(url)
    src = req.json()
    #проверяем существует ли директория с именем группы
    if os.path.exists(f'{group_name}'):
        print(f'Директория с именем {group_name} уже существует!')
    else:
        os.mkdir(group_name)

    with open(f'{group_name}/{group_name}.json', 'w', encoding='utf-8') as file:
        json.dump(src, file, indent=4, ensure_ascii=False)

    #собираем ID новых постов в список
    fresh_posts_id = []
    posts = src['response']['items']
    for fresh_post_id in posts:
        fresh_post_id = fresh_post_id['id']
        fresh_posts_id.append(fresh_post_id)

    # """Проверка первый ли это запуск или нет, если нет, то нужно сверять ID постов и заносить в файл только новые"""
    # if not os.path.exists(f'{group_name}/exist_posts_{group_name}.txt'):
    #     print('Файла с ID постов не существует, создаём файл!')
    #     with open(f'{group_name}/exist_posts_{group_name}.txt', 'w') as file:
    #         for item in fresh_posts_id:
    #             file.write(str(item) + '\n')

        #извлекаем данные из постов
    for post in posts:
        #функция для сохранения изображений
        def download_url(url, post_id, post_id_counter, group_name):
            res = requests.get(url)
            #создаём папку group_name/files
            if not os.path.exists(f'{group_name}/files'):
                os.mkdir(f'{group_name}/files')
            if not os.path.exists(f'{group_name}/files/{post_id}'):
                os.mkdir(f'{group_name}/files/{post_id}')

            with open(f'{group_name}/files/{post_id}/{post_id_counter}.jpg', 'wb') as img_file:
                img_file.write(res.content)
        #функция для сохрания текста поста
        def text_save(post_id, group_name):
            if not os.path.exists(f'{group_name}/text'):
                os.mkdir(f'{group_name}/text')
            if os.path.exists(f'{group_name}/text/{post_id}.txt'):
                pass
            else:
                with open(f'{group_name}/text/{post_id}.txt', 'w') as text_file:
                    text_file.write(post1)

        post_id = post['id']
        print(f'Отправляем пост с ID {post_id}')
        try:
            photo_post_count = 0
            if 'attachments' in post:
                post1 = post['text']
                post = post['attachments']
                if post[0]['type'] == 'photo':
                    if len(post) == 1:
                        post_photo = post[0]['photo']['sizes'][-1]['url']
                        download_url(post_photo, post_id, 0, group_name)
                        if len(post1) > 5:
                            text_save(post_id,group_name)
                    else:
                        if len(post1) > 5:
                            text_save(post_id, group_name)
                        for post_item_photo in post:
                            post_photo = post_item_photo['photo']['sizes'][-1]['url']
                            post_id_counter = str(post_id) + f'_{photo_post_count}'
                            download_url(post_photo, post_id, post_id_counter, group_name)
                            photo_post_count +=1

        except Exception:
            print(f'Что-то пошло не так c постом ID {post_id}!')


def main():
    n = int(input('Сколько сотен постов собрать?'))
    group_name = input('Введите название группы: ')
    offset = 0
    # owner_id = 'Название группы'
    owner_id = None
    for i in range(n):
        get_wall_posts(group_name, offset, owner_id)
        offset +=200
    for list1 in os.listdir(f'{group_name}/files'):
        for item in os.listdir(f'{group_name}/files/{list1}'):
            filename = f'{item}'
            path_full = f'{group_name}/files/{list1}/{item}'
            path = f'{group_name}/files/{list1}'
            wotemark_add.watermark(path_full, path, filename)

if __name__ == '__main__':
    main()