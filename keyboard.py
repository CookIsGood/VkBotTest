from vk_api.keyboard import VkKeyboard, VkKeyboardColor


# VkKeyboardColor.DEFAULT - белый цвет
# color=VkKeyboardColor.POSITIVE - зеленый
# color=VkKeyboardColor.NEGATIVE - красный
# color=VkKeyboardColor.PRIMARY - синий

def create_keyboard(response, user_id, my_id, id_1):
    keyboard = VkKeyboard(one_time=False)

    if response == 'начать':

        keyboard.add_button('О нас', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Команда 2', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Команда 3', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Команда 4', color=VkKeyboardColor.POSITIVE)
        if user_id == id_1 or user_id == my_id:
            keyboard.add_line()  # Переход на вторую строку
            keyboard.add_button('Рассылка', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_button('Закрыть клавиатуру', color=VkKeyboardColor.NEGATIVE)
    if (response == 'рассылка') and (user_id == id_1 or user_id == my_id):
        keyboard.add_button('Создать рассылку', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Отправить рассылку', color=VkKeyboardColor.NEGATIVE)

    elif response == 'закрыть клавиатуру':
        print('Закрываем клавиатуру')
        return keyboard.get_empty_keyboard()

    keyboard = keyboard.get_keyboard()
    return keyboard
