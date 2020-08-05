# vk-api
import vk_api
import vk_api.vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
# Приватные файлы
from login import vk_api_token, vk_id_group, my_id, vk_id_group_neg
# Вспомогательные библиотеки
import sqlite3
import threading
import time
import keyboard
import random
import datetime
import requests
import re
import sys


# KeyError:

def monitor_msg(vk_session, session_api, members):
    longpoll = VkLongPoll(vk_session)
    # users_not_msg = 0
    while True:
        try:
            for event in longpoll.listen():
                # Вывод сообщение по ивенту: НОВОЕ СООБЩЕНИЕ
                if event.type == VkEventType.MESSAGE_NEW:
                    print("Время сообщения: " + str(event.datetime))
                    print("Сообщение: " + str(event.text))
                    # Преобразование всего текста в нижний регистр
                    response = event.text.lower()
                    # Присоеденение к БД
                    # 0 - участник группы
                    # 1 - админ группы
                    # 2 - админ админов группы
                    if event.from_user and not event.from_me:
                        db = sqlite3.connect('server.db')
                        sql = db.cursor()
                        dataCopy = sql.execute(
                            f"SELECT permession  FROM users WHERE idlogin = '{event.user_id}' AND permession = '{1}'")
                        if dataCopy.fetchone() is None:
                            values = 0
                        else:
                            values = 1
                        db.close()
                        if event.user_id == my_id:
                            values = 2
                        new_keyboard = keyboard.create_keyboard(response, values)
                        # Если нажимают: "1"
                        if (response == 'рассылка') and (values == 1 or values == 2):
                            print("Ввели команду: рассылка")
                            with open("buff_text\Инструкция.txt", 'r', encoding="utf-8") as f:
                                message_main = f.read()
                            send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                         message=f"{message_main}",
                                         keyboard=new_keyboard, attachment=None)
                        elif response == 'начать' or response == 'вернуться назад':
                            with open("buff_text\Приветствие.txt", 'r', encoding="utf-8") as f:
                                message_main = f.read()
                            with open("buff_text\hello_for_users.txt", 'r', encoding="utf-8") as f:
                                hello_users = f.read()
                            name = session_api.users.get(user_ids=event.user_id)[0]["first_name"]
                            print("Ввели команду: начать")
                            if values == 1 or values == 2:
                              send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                           message=f"Привет, {name}! &#128127; {message_main}",
                                           keyboard=new_keyboard, attachment=None)
                            else:
                                send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                             message=f"Привет, {name}! {hello_users}",
                                             keyboard=new_keyboard, attachment=None)
                        elif response == 'о нас':
                            print("Ввели команду: о нас")
                            text_final = open("buff_text\аbout_text.txt", 'r', encoding="utf-8")
                            attach_final = open("buff_text\аbout_attach.txt", 'r', encoding="utf-8")
                            send_text_final = text_final.read()
                            send_attach_final = attach_final.read()
                            text_final.close()
                            attach_final.close()
                            send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                         message=f"{send_text_final}",
                                         keyboard=None, attachment=f"{send_attach_final}")
                        elif response == 'закрыть клавиатуру':
                            print("Ввели команду: закрыть клавиатуру")
                            send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                         message="Вы закрыли клавиатуру",
                                         keyboard=new_keyboard, attachment=None)
                        elif (response == 'создать рассылку') and (values == 1 or values == 2):
                            print("Ввели команду: создать рассылку")
                            send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                         message="Введите сообщение и прекрипите вложение!",
                                         keyboard=None, attachment=None)
                            text_send_in = open('buff_text\Текст рассылки.txt', 'w', encoding='utf-8')
                            attach_send_in = open('buff_text\Вложение рассылки.txt', 'w', encoding='utf-8')
                            text_send_in.truncate()
                            attach_send_in.truncate()
                        elif (response == 'отправить рассылку') and (values == 1 or values == 2):
                            text_final = open("buff_text\Текст рассылки.txt", 'r', encoding="utf-8")
                            attach_final = open("buff_text\Вложение рассылки.txt", 'r', encoding="utf-8")
                            send_text_final = text_final.read()
                            send_attach_final = attach_final.read()
                            text_final.close()
                            attach_final.close()
                            print("Список id участников группы: " + str(members))
                            print("Сообщение доставляется: " + str(len(members)) + " пользовтелям...")
                            # Цикл в котором будет происходить рассылка сообщения участникам группы
                            # Кол-во участников регулируется переменной count_users_items
                            for i in range(len(members)):
                                # users_not_msg += 1
                                # Блок try catch, если по каким то причинам невозможна отправка сообщения участнику,
                                # то добавляем к итератору 1 и продолжаем цикл for
                                try:
                                    send_message(vk_session, id_type='user_id', id_user=members[i],
                                                 message=f"{send_text_final}", keyboard=None,
                                                 attachment=f"{str(send_attach_final)}")
                                except vk_api.exceptions.ApiError:
                                    i += 1
                                    print("Пользователю не отправилось сообщение!")
                                    continue
                        elif (response == 'посмотреть рассылку') and (values == 1 or values == 2):
                            print("Ввели команду: посмотреть рассылку")
                            text_final = open("buff_text\Текст рассылки.txt", 'r', encoding="utf-8")
                            attach_final = open("buff_text\Вложение рассылки.txt", 'r', encoding="utf-8")
                            send_text_final = text_final.read()
                            send_attach_final = attach_final.read()
                            send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                         message=f"Обычная рассылка сообщений пользователям выглядит таким образом: \n\n\n {send_text_final}",
                                         keyboard=None, attachment=f"{send_attach_final}")
                        elif (response == 'управление админами') and (values == 1 or values == 2):
                            print("Ввели команду: управление админами")
                            with open("buff_text\control_admin.txt", 'r', encoding="utf-8") as f:
                                message_main = f.read()
                            send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                         message=f"{message_main}",
                                         keyboard=new_keyboard, attachment=None)
                            text_final = open("buff_text\Текст рассылки.txt", 'w', encoding="utf-8")
                            text_final.truncate()
                        elif (response == 'список админов') and (values == 1 or values == 2):
                            print("Ввели команду: список админов")
                            db = sqlite3.connect('server.db')
                            sql = db.cursor()
                            dataCount = sql.execute(
                                f"SELECT COUNT(idlogin)  FROM users WHERE permession = '{1}' OR permession = '{2}'")
                            numberOfRows = dataCount.fetchone()[0]
                            # reg = re.compile('[^a-zA-Z ]')
                            dataCopy = sql.execute(
                                f"SELECT idlogin  FROM users WHERE permession = '{1}' OR permession = '{2}'")
                            values = dataCopy.fetchmany(size=numberOfRows)
                            print("Кол во:" + str(numberOfRows))
                            print(type(values))
                            for i in range(0, numberOfRows):
                                send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                             message=f"Админ группы: id{values[i]}",
                                             keyboard=None, attachment=None)
                            text_final = open("buff_text\Текст рассылки.txt", 'w', encoding="utf-8")
                            text_final.truncate()
                        elif (response == 'добавить админа') and (values == 2):
                            print("Ввели команду: добавить админа")
                            send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                         message=f"Для того, чтобы добавить/удалить админа введите его id в формате: "
                                                 f"111111111 и отправьте его боту.\n А затем нажмите на кнопку "
                                                 f"сохранить добавление/удаление.",
                                         keyboard=None, attachment=None)
                            text_final = open("buff_text\id админа.txt", 'w', encoding="utf-8")
                            text_final.truncate()
                        elif (response == 'удалить админа') and (values == 2):
                            print("Ввели команду: удалить админа")
                            send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                         message=f"Для того, чтобы добавить/удалить админа введите его id в формате: "
                                                 f"111111111 и отправьте его боту.\n А затем нажмите на кнопку "
                                                 f"сохранить добавление/удаление.",
                                         keyboard=None, attachment=None)
                            text_final = open("buff_text\id админа.txt", 'w', encoding="utf-8")
                            text_final.truncate()
                        elif response == 'узнать id':
                            print("Ввели команду: узнать свой id")
                            send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                         message=f"Ваш id: {event.user_id}",
                                         keyboard=None, attachment=None)
                        elif response == 'сохранить добавление':
                            print("Ввели команду: Сохранить добавление")
                            text_final = open("buff_text\id админа.txt", 'r', encoding="utf-8")
                            send_text_final = text_final.read()
                            text_final.close()
                            db = sqlite3.connect('server.db')
                            sql = db.cursor()
                            sql.execute(
                                f'UPDATE users SET permession = {1} WHERE idlogin = "{send_text_final}"')
                            db.commit()
                            db.close()
                            send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                         message=f"Права обновлены!",
                                         keyboard=None, attachment=None)
                            text_final = open("buff_text\id админа.txt", 'w', encoding="utf-8")
                            text_final.truncate()
                        elif response == 'сохранить удаление':
                            print("Ввели команду: Сохранить удаление")
                            text_final = open("buff_text\id админа.txt", 'r', encoding="utf-8")
                            send_text_final = text_final.read()
                            text_final.close()
                            db = sqlite3.connect('server.db')
                            sql = db.cursor()
                            sql.execute(
                                f'UPDATE users SET permession = {0} WHERE idlogin = "{send_text_final}"')
                            db.commit()
                            db.close()
                            send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                         message=f"Права обновлены!",
                                         keyboard=None, attachment=None)
                            text_final = open("buff_text\id админа.txt", 'w', encoding="utf-8")
                            text_final.truncate()
                        elif (response == 'рассылкаопрос') and (values == 1 or values == 2):
                            print("Ввели команду: рассылкаопрос")
                            with open("buff_text\poll_msg.txt", 'r', encoding="utf-8") as f:
                                message_main = f.read()
                            send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                         message=f"{message_main}",
                                         keyboard=new_keyboard, attachment=None)
                        elif (response == 'посмотреть рассылку опроса') and (values == 1 or values == 2):
                            print("Ввели команду: посмотреть рассылку")
                            text_final = open("buff_text\Текст опрос.txt", 'r', encoding="utf-8")
                            attach_final = open("buff_text\Вложение опрос.txt", 'r', encoding="utf-8")
                            send_text_final = text_final.read()
                            send_attach_final = attach_final.read()
                            send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                         message=f"Рассылка для проголосовавших в опросе выглядит таким образом: \n\n\n{send_text_final}",
                                         keyboard=None, attachment=f"{send_attach_final}")
                        elif (response == 'создать сообщение') and (values == 1 or values == 2):
                            print("Ввели команду: создать сообщение")
                            send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                         message=f"Введите текст рассылки для проголосовавших в опросе и можете прикрепить "
                                                 f"вложения...",
                                         keyboard=None, attachment=None)
                            text_send_in = open('buff_text\Текст опрос.txt', 'w', encoding='utf-8')
                            attach_send_in = open('buff_text\Вложение опрос.txt', 'w', encoding='utf-8')
                            text_send_in.truncate()
                            attach_send_in.truncate()
                        elif (response == 'сохранить сообщение') and (values == 1 or values == 2):
                            print("Ввели команду: сохранить сообщение")
                            send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                         message=f"Текст рассылки для опроса успешно сохранен!",
                                         keyboard=None, attachment=None)
                        elif (response == 'создать id опроса') and (values == 1 or values == 2):
                            print("Ввели команду: создать id опроса")
                            send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                         message=f"Введите id опроса в формате: 111111111",
                                         keyboard=None, attachment=None)
                            text_send_in = open('buff_text\id опрос.txt', 'w', encoding='utf-8')
                            text_send_in.truncate()
                        elif (response == 'сохранить id опроса') and (values == 1 or values == 2):
                            print("Ввели команду: сохранить id опроса")
                            send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                         message=f"Id опроса успешно сохранен!",
                                         keyboard=None, attachment=None)
                        elif (response == "создать о нас") and (values == 1 or values == 2):
                            print("Ввели команду: создать о нас")
                            with open("buff_text\create_about.txt", 'r', encoding="utf-8") as f:
                                message_main = f.read()
                            send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                         message=f"{message_main}",
                                         keyboard=new_keyboard, attachment=None)
                        elif (response == 'создать текст') and (values == 1 or values == 2):
                            print("Ввели команду: создать текст")
                            send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                         message=f"Введите текст и прекрепите вложение, а потом отправьте это "
                                                 f"сообщение боту. \n Затем, нажмите кнопку: сохранить текст",
                                         keyboard=None, attachment=None)
                            text_send_in = open('buff_text\аbout_text.txt', 'w', encoding='utf-8')
                            attach_send_in = open('buff_text\аbout_attach.txt', 'w', encoding='utf-8')
                            text_send_in.truncate()
                            attach_send_in.truncate()
                        elif (response == 'сохранить текст') and (values == 1 or values == 2):
                            print("Ввели команду: сохранить текст")
                            send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                         message=f"Ваш текст сохранен! Проверьте кнопку: О нас",
                                         keyboard=None, attachment=None)
                        elif (response == 'посмотреть о нас') and (values == 1 or values == 2):
                            print("Ввели команду: Посмотреть о нас")
                            text_send_in = open('buff_text\аbout_text.txt', 'r', encoding='utf-8')
                            attach_send_in = open('buff_text\аbout_attach.txt', 'r', encoding='utf-8')
                            send_text_final = text_send_in.read()
                            send_attach_final = attach_send_in.read()

                            send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                         message=f"Пункт меню О нас - выглядит таким образом: \n\n\n{send_text_final}",
                                         keyboard=None, attachment=f"{send_attach_final}")
                        elif values == 1 or values == 2:
                            msg_history = vk_session.method('messages.getHistory',
                                                            {'offset': 2, 'count': 1, 'user_id': event.user_id,
                                                             'group_id': vk_id_group})
                            msg_text = msg_history["items"][0]["text"]
                            print("ОБРАТИ НА МЕНЯ ВНИМАНИЕ: " + str(msg_text))
                            if msg_text == 'создать рассылку' or msg_text == 'Создать рассылку':
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
                                buff = []
                                for i in range(0, len(buff_type)):
                                    buff.append(str(buff_type[i]) + str(buff_id[i]))
                                final_buff = []
                                for items in buff:
                                    final_buff.append(items)
                                attach_list = ','.join(final_buff)
                                text_final = open("buff_text\Текст рассылки.txt", 'r+', encoding="utf-8")
                                attach_final = open("buff_text\Вложение рассылки.txt", 'r+', encoding="utf-8")
                                new_text_send = text_final.read()
                                new_attach_send = attach_final.read()
                                new_text_send = re.sub(new_text_send, str(event.text), new_text_send)
                                new_attach_send = re.sub(new_attach_send, str(attach_list), new_attach_send)
                                text_final.write(new_text_send)
                                attach_final.write(new_attach_send)
                                text_final.close()
                                attach_final.close()
                            elif msg_text == 'создать сообщение' or msg_text == 'Создать сообщение':
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
                                buff = []
                                for i in range(0, len(buff_type)):
                                    buff.append(str(buff_type[i]) + str(buff_id[i]))
                                final_buff = []
                                for items in buff:
                                    final_buff.append(items)
                                attach_list = ','.join(final_buff)
                                text_final = open("buff_text\Текст опрос.txt", 'r+', encoding="utf-8")
                                attach_final = open("buff_text\Вложение опрос.txt", 'r+', encoding="utf-8")
                                new_text_send = text_final.read()
                                new_attach_send = attach_final.read()
                                new_text_send = re.sub(new_text_send, str(event.text), new_text_send)
                                new_attach_send = re.sub(new_attach_send, str(attach_list), new_attach_send)
                                text_final.write(new_text_send)
                                attach_final.write(new_attach_send)
                                text_final.close()
                                attach_final.close()
                            elif msg_text == 'cоздать id опроса' or msg_text == 'Создать id опроса':
                                text_final = open("buff_text\id опрос.txt", 'r+', encoding="utf-8")
                                new_text_send = text_final.read()
                                new_text_send = re.sub(new_text_send, str(event.text), new_text_send)
                                text_final.write(new_text_send)
                                text_final.close()
                            elif msg_text == 'добавить админа' or msg_text == 'Добавить админа':
                                text_final = open("buff_text\id админа.txt", 'r+', encoding="utf-8")
                                new_text_send = text_final.read()
                                new_text_send = re.sub(new_text_send, str(event.text), new_text_send)
                                text_final.write(new_text_send)
                                text_final.close()
                            elif msg_text == 'удалить админа' or msg_text == 'Удалить админа':
                                text_final = open("buff_text\id админа.txt", 'r+', encoding="utf-8")
                                new_text_send = text_final.read()
                                new_text_send = re.sub(new_text_send, str(event.text), new_text_send)
                                text_final.write(new_text_send)
                                text_final.close()
                            elif msg_text == 'cоздать текст' or msg_text == 'Создать текст':
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
                                buff = []
                                for i in range(0, len(buff_type)):
                                    buff.append(str(buff_type[i]) + str(buff_id[i]))
                                final_buff = []
                                for items in buff:
                                    final_buff.append(items)
                                attach_list = ','.join(final_buff)
                                text_final = open("buff_text\аbout_text.txt", 'r+', encoding="utf-8")
                                attach_final = open("buff_text\аbout_attach.txt", 'r+', encoding="utf-8")
                                new_text_send = text_final.read()
                                new_attach_send = attach_final.read()
                                new_text_send = re.sub(new_text_send, str(event.text), new_text_send)
                                new_attach_send = re.sub(new_attach_send, str(attach_list), new_attach_send)
                                text_final.write(new_text_send)
                                attach_final.write(new_attach_send)
                                text_final.close()
                                attach_final.close()
                            else:
                                print("Неопозннная команда...")
                                send_message(vk_session, id_type='user_id', id_user=event.user_id,
                                             message=f"Я тебя не понимаю. \nДля того, чтобы посмотреть мои команды введи: начать",
                                             keyboard=None, attachment=None)

        except Exception as error:
            print(error)


# Функция отвечающая за отправку сообщений участникам
def send_message(vk_session, id_type, id_user, message=None, keyboard=None, attachment=None):
    vk_session.method('messages.send',
                      {id_type: id_user, 'message': message, 'random_id': random.randint(-2147483648, +2147483648),
                       'keyboard': keyboard, "attachment": attachment})


# Исполняющая программу функция
def main():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute("""CREATE TABLE IF NOT EXISTS users (
              idlogin TEXT,
              permession INT,
              UNIQUE(idlogin)
              )""")
    sql.execute(f"INSERT OR IGNORE INTO users VALUES ('{my_id}', '{2}')")
    db.commit()
    # vk-api (longpool)
    vk_session = vk_api.VkApi(token=vk_api_token)
    session_api = vk_session.get_api()
    members_count = vk_session.method('groups.getById', {'group_id': vk_id_group, 'fields': "members_count"})
    count_ids = members_count[0]["members_count"]

    # Присваиваем id участников в отдельную переменную
    members = []
    if count_ids > 1000:
        for i in range(0, 1 + count_ids // 1000):
            members.extend(vk_session.method('groups.getMembers', {'group_id': vk_id_group, 'count': 1000, 'offset': i * 1000})["items"])
            print("Добавил" + str(i))
    else:
        members = vk_session.method('groups.getMembers', {'group_id': vk_id_group, 'count': 1000})["items"]
        print("Добавил все else")
    # Получаем количество участников группы
    for i in range(count_ids):
        sql.execute(f"INSERT OR IGNORE INTO users VALUES ('{members[i]}', '{0}')")
        db.commit()
    db.close()
    print("Приложение запущено")
    monitor_msg(vk_session, session_api, members)


if __name__ == '__main__':
    main()
