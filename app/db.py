import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime


Base = declarative_base()

engine = sq.create_engine('postgresql+psycopg2://kola:super123@localhost:5432/date')
Session = sessionmaker(bind=engine)


class Username(Base):
    __tablename__ = 'username'
    id = sq.Column(sq.Integer,primary_key=True)
    vk_id = sq.Column(sq.Integer)
    fname = sq.Column(sq.String)
    lname = sq.Column(sq.String)
    age = sq.Column(sq.Integer)
    age_from = sq.Column(sq.Integer)
    age_to = sq.Column(sq.Integer)
    city_id = sq.Column(sq.String)
    city_name = sq.Column(sq.String)
    datinguser = relationship('DatingUser', backref='username')


class DatingUser(Base):
    __tablename__ = 'datinguser'
    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer)
    fname = sq.Column(sq.String)
    lname = sq.Column(sq.String)
    age = sq.Column(sq.String)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('username.id'))
    photos = relationship('Photos', backref='datinguser')


class Photos(Base):
    __tablename__ = 'photo'
    id = sq.Column(sq.Integer, primary_key = True)
    id_datinguser = sq.Column(sq.Integer, sq.ForeignKey('datinguser.id'))
    link_photo = sq.Column(sq.String)
    count_likes = sq.Column(sq.Integer)

# Создание записи в БД user
def user_record(dict_user):
    session = Session()
    query = session.query(Username).all()
    if dict_user['id'] in [user.vk_id for user in query]:
        return [dict_user['first_name'],dict_user['id']]
    print('Введите предпочитаемый возраст поиска')
    age_from = input('От: ')
    age_to = input('До: ')
    age = bdate(dict_user)
    id_user = Username(vk_id = dict_user['id'], fname = dict_user['first_name'],
    lname = dict_user['last_name'],age = age, age_from = age_from, age_to = age_to,
    city_id = dict_user['city']['id'],city_name = dict_user['city']['title'])
    session.add(id_user)
    session.commit()
    return dict_user['first_name'],dict_user['id']

#Просчет возраста из полученных данных с аккаунта
def bdate(dict_user):
    now = datetime.now()
    year = now.year
    date = dict_user['bdate']
    age = year - int(''.join(date.split('.')[2]))
    return age

#Ввод данных для поиска пары
def info_user_search(id):
    session = Session()
    query = session.query(Username).filter(Username.vk_id == id).all()
    search_info = {'age_from':'', 'age_to': '', 'city_id':'','sex':''}
    search_info['sex'] = input('Введите пол кого вы хотите найти (1 - девушку, 2 - мужчину:) ')
    for user in query:
        search_info['city_id'] = user.city_id
        search_info['age_from'] = user.age_from
        search_info['age_to'] = user.age_to
    print('Введите возраст для поиска людей')
    print(f'Y - оставить  от {user.age_from} до {user.age_to}')
    print(f'N - ввести новые параметры:')
    age_requests = input('Выберите параметр: ')
    if age_requests == 'N':
        search_info['age_from'] = input('Введите возраст от: ')
        search_info['age_to'] = input('Введите возраст до: ')
    return search_info

# Запсь в бд понравившегося человека и 3х лучших фото
def dating_user_record(list_dating,id):
    session = Session()
    query = session.query(Username).filter(Username.vk_id == id).first()
    id_user = query.id
    dating_user = DatingUser(vk_id = int(list_dating[0]), fname = list_dating[2], lname = list_dating[3],age = list_dating[1],id_user = id_user)
    session.add(dating_user)
    session.commit()
    query_dating = session.query(DatingUser).filter(DatingUser.vk_id == int(list_dating[0])).first()
    for photo in list_dating[4:]:
        photo_dating = Photos(id_datinguser = query_dating.id,link_photo = photo[1],count_likes = int(photo[0]))
        session.add(photo_dating)
        session.commit()
    return True

# функции проверки наличия профиля уже в отмеченных   
def dating_user_norepeat(id):
    session = Session()
    query = session.query(DatingUser).all()
    if id in [user.vk_id for user in query]:
        return True
    return False

# Вывод всех избранных пользователей 
def dating_user_list(id):
    session = Session()
    query = session.query(Username).filter(Username.vk_id == id).first()
    query_2 = session.query(DatingUser).filter(DatingUser.id_user == query.id).all()
    dating_user_list = []
    for user in query_2:
        dtuser = []
        dtuser.append(user.vk_id)
        dtuser.append(user.age)
        dtuser.append(user.fname)
        dtuser.append(user.lname)
        q = session.query(Photos).filter(Photos.id_datinguser == user.id).all()
        for photo in q:
            dtuser.append(photo.link_photo)
        dating_user_list.append(dtuser)
    return dating_user_list

# Удаление из списка избранных
def dating_user_delete(id):
    session = Session()
    query = session.query(DatingUser).filter(DatingUser.vk_id == id).first()
    session.query(Photos).filter(Photos.id_datinguser == query.id).delete()
    session.query(DatingUser).filter(DatingUser.vk_id == id).delete()
    session.commit()