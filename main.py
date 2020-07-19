import requests
import vk_api
import vk_api.vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from login import vk_api_token
# Импортируем созданный нами класс Server
from server import Server
import random


def monitor_msg(vk_session):
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print("Время сообщения: " + str(event.datetime))
            print("Сообщение: " + str(event.text))
            response = event.text.lower()
            if event.from_user and not event.from_me:
                if response == '1':
                    send_message(vk_session, 'user_id', event.user_id,
                                 message=get_members(vk_session))


def send_message(vk_session, id_type, id, message=None):
    vk_session.method('messages.send',
                      {id_type: id, 'message': message, 'random_id': random.randint(-2147483648, +2147483648)})


def get_members(vk_session, group_id="197230708", count=1000):
    vk_session.method('groups.getMembers',
                      {'group_id': group_id, 'count': count})


def main():
    vk_session = vk_api.VkApi(token=vk_api_token)

    monitor_msg(vk_session)

    # server1 = Server(vk_api_token, 197230708, "server1")
    # vk_api_token - API токен, который мы ранее создали
    # 172998024 - id сообщества-бота
    # "server1" - имя сервера

    # server1.test()
    # send_message(vk_session, "user_id", 114220893, message="Привет")


if __name__ == '__main__':
    main()
