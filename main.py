import requests
import vk_api
import vk_api.vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from login import vk_api_token, vk_id_group
import random


def monitor_msg(vk_session):
    longpoll = VkLongPoll(vk_session)
    # users_not_msg = 0
    for event in longpoll.listen():
        # Вывод сообщение по ивенту: НОВОЕ СООБЩЕНИЕ
        if event.type == VkEventType.MESSAGE_NEW:
            print("Время сообщения: " + str(event.datetime))
            print("Сообщение: " + str(event.text))
            # Преобразование всего текста в нижний регистр
            response = event.text.lower()
            if event.from_user and not event.from_me:
                # Если нажимают: "1"
                if response == '1':
                    # Вытаскиваем всех участников группы для получения их id
                    members = vk_session.method('groups.getMembers',
                                                {'group_id': vk_id_group, 'count': 20})
                    # Присваиваем id участников в отдельную переменную
                    users_items = members["items"]
                    # Получаем количество участников группы
                    count_users_items = members["count"]
                    print("Список id участников группы: " + str(users_items))
                    print("Сообщение доставляется: " + str(count_users_items) + " пользовтелям...")
                    # Цикл в котором будет происходить рассылка сообщения участникам группы
                    # Кол-во участников регулируется переменной count_users_items
                    for i in range(count_users_items):
                        # users_not_msg += 1
                        # Блок try catch, если по каким то причинам невозможна отправка сообщения участнику,
                        # то добавляем к итератору 1 и продолжаем цикл for
                        try:
                            send_message(vk_session, id_type='user_id', id_user=users_items[i],
                                         message="Привет!")
                        except vk_api.exceptions.ApiError:
                            i += 1
                            print("Пользователю не отправилось сообщение!")
                            continue


# Функция отвечающая за отправку сообщений участникам
def send_message(vk_session, id_type, id_user, message=None):
    vk_session.method('messages.send',
                      {id_type: id_user, 'message': message, 'random_id': random.randint(-2147483648, +2147483648)})


# Исполняющая программу функция
def main():
    print("приложение запущено")
    vk_session = vk_api.VkApi(token=vk_api_token)
    monitor_msg(vk_session)


if __name__ == '__main__':
    main()
