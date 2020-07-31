from vk_api.keyboard import VkKeyboard, VkKeyboardColor


# VkKeyboardColor.DEFAULT - белый цвет
# color=VkKeyboardColor.POSITIVE - зеленый
# color=VkKeyboardColor.NEGATIVE - красный
# color=VkKeyboardColor.PRIMARY - синий

def create_keyboard(response, values):
    keyboard = VkKeyboard(one_time=False)

    if response == 'начать' or response == 'вернуться назад':

        keyboard.add_button('О нас', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Узнать id', color=VkKeyboardColor.POSITIVE)
        if values == 1 or values == 2:
            keyboard.add_line()  # Переход на вторую строку
            keyboard.add_button('Рассылка', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button('РассылкаОпрос', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_line()
            keyboard.add_button('Управление админами', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_line()
            keyboard.add_button('Создать о нас', color=VkKeyboardColor.NEGATIVE)
    if (response == 'рассылка') and (values == 1 or values == 2):
        keyboard.add_button('Создать рассылку', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Посмотреть рассылку', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_button('Отправить рассылку', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_button('Вернуться назад', color=VkKeyboardColor.PRIMARY)
    if (response == 'управление админами') and (values == 1 or values == 2):
        keyboard.add_button('Список админов', color=VkKeyboardColor.POSITIVE)
        if values == 2:
            keyboard.add_line()
            keyboard.add_button('Добавить админа', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button('Сохранить добавление', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_line()
            keyboard.add_button('Удалить админа', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button('Сохранить удаление', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_button('Вернуться назад', color=VkKeyboardColor.PRIMARY)
    if (response == 'рассылкаопрос') and (values == 1 or values == 2):
        keyboard.add_button('Создать сообщение', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Сохранить сообщение', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_button('Создать id опроса', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Сохранить id опроса', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_button('Посмотреть рассылку опроса', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_button('Вернуться назад', color=VkKeyboardColor.PRIMARY)
    if (response == 'создать о нас') and (values == 1 or values == 2):
        keyboard.add_button('Создать текст', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Сохранить текст', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_button('Вернуться назад', color=VkKeyboardColor.PRIMARY)
    elif response == 'закрыть клавиатуру':
        print('Закрываем клавиатуру')
        return keyboard.get_empty_keyboard()

    keyboard = keyboard.get_keyboard()
    return keyboard