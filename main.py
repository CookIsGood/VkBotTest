import requests

import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import login


def main():
    token = login.TokenR()
    vk_session = vk_api.VkApi(token=token)
    longpoll = VkLongPoll(vk_session)
    while True:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                print("Время сообщения: " + str(event.datetime))
                print("Сообщение: " + str(event.text))
                print("Список участников: " + str())


if __name__ == '__main__':
    main()
