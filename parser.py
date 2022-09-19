import os


def main(dir_name):
    l2 = []
    for list1 in os.listdir(f'{dir_name}/files'):
        s = ''
        l2.append(list1)
        try:
            with open(f'{dir_name}/text/{list1}.txt', 'r') as text_file:
                text = text_file.readlines()
                for i in text:
                    if i == 'Строка, которую будем удалять':
                        pass
                    else:
                        s+=i
            with open(f'{dir_name}/text/{list1}.txt', 'w') as text_file:
                text_file.write(s)
        except IndexError:
            print('Кажется документ пустой')

if __name__ == '__main__':
    main('a')