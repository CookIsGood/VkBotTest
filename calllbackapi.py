# vk
import vk
# Приватные файлы
from login import confirmation_token, vk_api_token
# Вспомогательные библиотеки
from flask import Flask, request, json
import random

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
