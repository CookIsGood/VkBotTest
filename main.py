# vk-api
import vk_api
import vk_api.vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType

# print(vk_api.path)
from vk_api.utils import get_random_id
# Приватные файлы
from login import vk_api_token, vk_id_group, my_id, id_1
import video_get
# Вспомогательные библиотеки
import keyboard
import random
import datetime
import requests
import re
import sys


# KeyError:

def monitor_msg(vk_session, session_api):
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        # Вывод сообщение по ивенту: НОВОЕ СООБЩЕНИЕ
        if event.type == VkEventType.POLL_VOTE_NEW:
            print("Время сообщения: " + str(event.datetime))
            print("Сообщение: " + str(event.text))
            # Преобразование всего текста в нижний регистр
            response = event.text.lower()
            new_keyboard = keyboard.create_keyboard(response, event.user_id, my_id, id_1)
            if event.from_user and not event.from_me:
                # Если нажимают: "1"
                if (response == 'рассылка') and (event.user_id == id_1 or event.user_id == my_id):
                    send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                 message="Вы попали в меню рассылки!",
                                 keyboard=new_keyboard, attachment=None)
                elif response == 'начать':
                    with open("Приветствие.txt", 'r', encoding="utf-8") as f:
                        message_main = f.read()
                    name = session_api.users.get(user_ids=event.user_id)[0]["first_name"]
                    print("Ввели команду: начать")
                    send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                 message=f"Привет, {name}! &#128127; {message_main}",
                                 keyboard=new_keyboard, attachment=None)
                elif response == 'о нас':
                    print("Ввели команду: о нас")
                    attach = 'video-191447820_456239018', 'photo114220893_457247628'
                    print(type(attach))
                    buff = []
                    for items in attach:
                        buff.append(items)
                    attach_list = ','.join(buff)
                    print(attach_list)
                    send_message(vk_session, id_type='user_id', id_user=event.user_id, message="Ссылка на видео",
                                 keyboard=None, attachment=attach_list)
                elif response == 'команда 2':
                    print("Ввели команду: команда 2")
                    send_message(vk_session, id_type='user_id', id_user=event.user_id, message="Вы ввели команду 2",
                                 keyboard=None, attachment=None)
                elif response == 'команда 3':
                    print("Ввели команду: команда 3")
                    send_message(vk_session, id_type='user_id', id_user=event.user_id, message="Вы ввели команду 3",
                                 keyboard=None, attachment=None)
                elif response == 'команда 4':
                    print("Ввели команду: команда 4")
                    send_message(vk_session, id_type='user_id', id_user=event.user_id, message="Вы ввели команду 4",
                                 keyboard=None, attachment=None)
                elif response == 'закрыть клавиатуру':
                    print("Ввели команду: закрыть клавиатуру")
                    send_message(vk_session, id_type='user_id', id_user=event.user_id, message="Вы закрыли клавиатуру",
                                 keyboard=new_keyboard, attachment=None)
                elif (response == 'создать рассылку') and (event.user_id == id_1 or event.user_id == my_id):
                    with open("Инструкция.txt", 'r', encoding="utf-8") as f:
                        message_main = f.read()
                    print("Ввели команду: создать рассылку")
                    send_message(vk_session, id_type='user_id', id_user=event.user_id, message=f"{message_main}",
                                 keyboard=None, attachment=None)
                    text_send_in = open('Текст рассылки.txt', 'w', encoding='utf-8')
                    attach_send_in = open('Вложение рассылки.txt', 'w', encoding='utf-8')
                    text_send_in.truncate()
                    attach_send_in.truncate()
                elif (response == 'отправить рассылку') and (event.user_id == id_1 or event.user_id == my_id):
                    text_final = open("Текст рассылки.txt", 'r', encoding="utf-8")
                    attach_final = open("Вложение рассылки.txt", 'r', encoding="utf-8")
                    send_text_final = text_final.read()
                    send_attach_final = attach_final.read()
                    text_final.close()
                    attach_final.close()
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
                                         message=f"{send_text_final}", keyboard=None,
                                         attachment=f"{str(send_attach_final)}")
                        except vk_api.exceptions.ApiError:
                            i += 1
                            print("Пользователю не отправилось сообщение!")
                            continue
                else:
                    print(event.attachments)
                    buff_type = []
                    buff_id = []
                    for i in range(1, 10):
                        try:
                            id_attach = event.attachments["attach" + str(i)]
                            buff_id.append(id_attach)
                            type_attach = event.attachments["attach" + str(i) + "_type"]
                            buff_type.append(type_attach)
                        except KeyError:
                            pass
                    print(len(buff_type))
                    print(buff_id)
                    buff = []
                    for i in range(0, len(buff_type)):
                        buff.append(str(buff_type[i]) + str(buff_id[i]))
                    print(buff)
                    final_buff = []
                    for items in buff:
                        final_buff.append(items)
                    attach_list = ','.join(final_buff)
                    text_final = open("Текст рассылки.txt", 'r+', encoding="utf-8")
                    attach_final = open("Вложение рассылки.txt", 'r+', encoding="utf-8")
                    new_text_send = text_final.read()
                    new_attach_send = attach_final.read()
                    new_text_send = re.sub(new_text_send, str(event.text), new_text_send)
                    new_attach_send = re.sub(new_attach_send, str(attach_list), new_attach_send)
                    text_final.write(new_text_send)
                    attach_final.write(new_attach_send)
                    text_final.close()
                    attach_final.close()


# Функция отвечающая за отправку сообщений участникам
def send_message(vk_session, id_type, id_user, message=None, keyboard=None, attachment=None):
    vk_session.method('messages.send',
                      {id_type: id_user, 'message': message, 'random_id': random.randint(-2147483648, +2147483648),
                       'keyboard': keyboard, "attachment": attachment})


# Исполняющая программу функция
def main():
    print("Приложение запущено")
    vk_session = vk_api.VkApi(token=vk_api_token)
    session_api = vk_session.get_api()
    monitor_msg(vk_session, session_api)


if __name__ == '__main__':
    main()
