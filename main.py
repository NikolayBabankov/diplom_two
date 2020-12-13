import vk_api
from pprint import pprint
from app.db import user_record,info_user_search, bdate, dating_user_record,dating_user_norepeat,dating_user_list,dating_user_delete
from collections import Counter
from operator import itemgetter


# Поиск подходящих аккаунтов со статусами:не женат/не замужем и в активном поиске
def choice_dating_user(dict_user):
    user_list = []
    status = 1
    while status < 7:
        search_id_dict = vk.users.search(sex=dict_user['sex'],city=dict_user['city_id'],
        age_from = dict_user['age_from'],age_to = dict_user['age_to'] ,status = status,count = 900)
        for user in search_id_dict['items']:
            if not user['is_closed']:
                user_list.append(user['id'])
        status += 5
    user_set = set(user_list)
    return user_set

#выборка 3х фото с наибольшим количеством лайков
def photo_user(id):
    photos = vk.photos.getAll(owner_id=id,extended=1,photo_sizes= 1,count = 100)
    list_photos = photos['items']
    index_list = []
    values_list = []
    for index, item in enumerate(list_photos):
        index_list.append(index)
        values_list.append(item['likes']['count'])

    likes_dict = dict(zip(index_list,values_list))
    sort_dict = Counter(likes_dict)
    likes = sort_dict.most_common()
    likes_photo = []
    for index,i in enumerate(likes):
        if index > 2:
            break
        x = list(i)
        likes_photo.append(x[0])
    url_photo = []
    for i in likes_photo:
        photo_url = list_photos[i]['sizes']
        count_likes = list_photos[i]['likes']['count']
        sorted_dict = sorted(photo_url, key=itemgetter('width','height'))
        file_url = sorted_dict[-1]['url']
        photo_list_likes =[]
        photo_list_likes.append(count_likes)
        photo_list_likes.append(file_url)
        url_photo.append(photo_list_likes)
    return url_photo

#Вывод информации и фото
def dating_user(id):
    info = vk.users.get(user_ids = id,fields = 'bdate')
    info_list = []
    info_list.append(id)
    try:
        info_list.append(bdate(info[0]))
    except:
        info_list.append('-')
    info_list.append(info[0]['first_name'])
    info_list.append(info[0]['last_name'])
    photo = photo_user(id)
    dating_user = info_list + photo
    return dating_user

# текстовое меню и ввод данных и команд от пользователя
if __name__ == "__main__":
    print('VKinder - программа поиска людей для знакомств из социальной сети Вконтаке')
    login = input('Введите логин: ')
    password = input('Введите пароль: ')
    vk_session = vk_api.VkApi(login, password)
    vk_session.auth()
    vk = vk_session.get_api()
    user_info = vk.account.getProfileInfo()
    user = user_record(user_info)
    print(f'Добрый день! {user[0]}')
    id_user = int(user_info['id'])
    user_search = info_user_search(user[1])
    list_user_dating = choice_dating_user(user_search)
    while True:
        print()
        print('f-начать поиск')
        print('b - вывести список избранных пользователей')
        print('q-выйти')
        user_input = input('Введите команду: ')
        if user_input == 'f':
            for dtuser in list_user_dating:
                if dating_user_norepeat(dtuser):
                    continue
                list_seacrh_user = dating_user(dtuser)
                print()
                print(f'Имя: {list_seacrh_user[2]}  | Фамилия: {list_seacrh_user[3]}  | Возраст: {list_seacrh_user[1]} | ID: {list_seacrh_user[0]}')
                for ph in list_seacrh_user[4:]:
                    print('Фото----------------------------')
                    print(ph[1])
                print()
                input_command = input('Введите команду(n - следующий человек, s - сохранить в избранное, q - выйти): ')
                if input_command == 'n':
                    continue
                if input_command == 's':
                    dating_user_record(list_seacrh_user,id_user)
                if input_command == 'q':
                    break
        elif user_input == 'b':
            best_list = dating_user_list(id_user)
            for user in best_list:
                print()
                print(f'Имя: {user[2]}  | Фамилия: {user[3]}  | Возраст: {user[1]} | ID: {user[0]}')
                for ph in user[4:]:
                    print('Фото----------------------------')
                    print(ph)
                print()
            print('Введите id пользователя, которого хотите удалить, пропустить этот шаг введите "e" ')
            id_del = input('Ввод: ')
            if id_del == 'e':
                continue
            else:
                try:
                    dating_user_delete(int(id_del))
                except:
                    print('Такого пользователя нет')
                    continue
        elif user_input == 'q':
            print('До свидания')
            break
