# vk
import vk
# vk-api
import vk_api
import vk_api.vk_api
# Приватные файлы
from login import confirmation_token, vk_api_token, vk_token_server, vk_id_group, my_id
# Вспомогательные библиотеки
from flask import Flask, request, json
import random
import sqlite3

app = Flask(__name__)


# callback API

@app.route('/')
def hello_world():
    return 'Hello from Flask!'


@app.route('/', methods=['POST'])
def processing():
    # Распаковываем json из пришедшего POST-запроса
    data = json.loads(request.data)

    # Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'poll_vote_new':
        session = vk.Session()
        # vk_session = vk_api.VkApi(token=vk_api_token)
        api = vk.API(session, v='5.110')
        # session_api = vk_session.get_api()
        user_id = data['object']['user_id']
        api.messages.send(access_token=vk_api_token, user_id=str(user_id), message='Привет, я новый бот!',
                          attachment='photo114220893_457247628', random_id=random.getrandbits(64))
        # Сообщение о том, что обработка прошла успешно
        return 'ok'
    elif data['type'] == 'group_join':
        vk_session_server = vk_api.VkApi(token=vk_token_server)
        db = sqlite3.connect('server.db')
        sql = db.cursor()
        sql.execute("""CREATE TABLE IF NOT EXISTS users (
              idlogin TEXT,
              permession INT
              )""")
        db.commit()
        # Вытаскиваем всех участников группы для получения их id
        members = vk_session_server.method('groups.getMembers',
                                           {'group_id': vk_id_group, 'count': 1000})
        # Присваиваем id участников в отдельную переменную
        users_items = members["items"]
        session = vk.Session()
        api = vk.API(session, v='5.110')
        user_id = data['object']['user_id']
        # Получаем количество участников группы
        count_users_items = members["count"]
        # sql.execute(f"INSERT INTO users VALUES ({id_users}, '{0}')")
        # db.commit()
        for i in range(count_users_items):
            dataCopy = sql.execute("SELECT idlogin  FROM users")
            if dataCopy.fetchone() is None:
                sql.execute(f"INSERT INTO users VALUES ({users_items[i]}, '{0}')")
                db.commit()
                api.messages.send(access_token=vk_api_token, user_id=str(my_id), message=f'В группу вступил: {users_items[i]}', random_id=random.getrandbits(64))
            else:
                api.messages.send(access_token=vk_api_token, user_id=str(my_id), message=f'Пользователь уже вступил: {users_items[i]}', random_id=random.getrandbits(64))
        # values = dataCopy.fetchone()
        db.close()
        return 'ok'
