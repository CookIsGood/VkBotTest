import vk_api.vk_api

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType


class Server:

    def __init__(self, api_token, group_id, server_name: str = "Empty"):
        # Даем серверу имя
        self.server_name = server_name

        # Для Long Poll

        self.vk = vk_api.VkApi(token=api_token)

        # Для использования Long Poll API
        self.long_poll = VkBotLongPoll(self.vk, group_id)

        # Для вызова методов vk_api
        self.vk_api = self.vk.get_api()

    def send_msg(self, send_id, message):
        """
        Отправка сообщения через метод messages.send
        :param send_id: vk id пользователя, который получит сообщение
        :param message: содержимое отправляемого письма
        :return: None
        """
        self.vk_api.messages.send(user_id=send_id,
                                  message=message,  random_id=random.randint(0, 2048))

    def test(self):
        # Посылаем сообщение пользователю с указанным ID
        self.send_msg(114220893, "Привет-привет!")
