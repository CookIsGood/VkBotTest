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
    poll_id = open("id опрос.txt", 'r+', encoding="utf-8")
    poll_text = open("Текст опрос.txt", 'r+', encoding="utf-8")
    poll_attach = open("Вложение опрос.txt", 'r+', encoding="utf-8")
    poll_id_read = poll_id.read()
    poll_text_read = poll_text.read()
    poll_attach_read = poll_attach.read()
    # Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'poll_vote_new' and data['object']['poll_id'] == int(poll_id_read):
        session = vk.Session()
        # vk_session = vk_api.VkApi(token=vk_api_token)
        api = vk.API(session, v='5.110')
        # session_api = vk_session.get_api()
        user_id = data['object']['user_id']
        api.messages.send(access_token=vk_api_token, user_id=str(user_id), message=f'{poll_text_read}',
                          attachment=f'{poll_attach_read}', random_id=random.getrandbits(64))
        # Сообщение о том, что обработка прошла успешно
        return 'ok'
    elif data['type'] == 'group_join':
        # vk_session_server = vk_api.VkApi(token=vk_token_server)
        db = sqlite3.connect('server.db')
        sql = db.cursor()
        sql.execute("""CREATE TABLE IF NOT EXISTS users (
              idlogin TEXT,
              permession INT,
              UNIQUE(idlogin, permession)
              )""")
        db.commit()
        session = vk.Session()
        api = vk.API(session, v='5.110')
        user_id = data['object']['user_id']
        dataCopy = sql.execute(f"SELECT idlogin  FROM users WHERE idlogin = '{user_id}'")
        if dataCopy.fetchone() is None:
            sql.execute(f"INSERT OR IGNORE INTO users VALUES ('{user_id}', '{0}')")
            db.commit()
            api.messages.send(access_token=vk_api_token, user_id=str(my_id), message=f'В группу вошел: {user_id}', random_id=random.getrandbits(64))
        else:
            api.messages.send(access_token=vk_api_token, user_id=str(my_id), message=f'Уже в группе: {user_id}', random_id=random.getrandbits(64))
        # values = dataCopy.fetchone()
        db.close()
        return 'ok'