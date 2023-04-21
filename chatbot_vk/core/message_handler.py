from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from .gpt import get_gpt_response
from db import models
import random
import time

def send_message(vk, user_id, message, keyboard=None):
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=random.randint(1, 2 ** 32),
        keyboard=keyboard.get_keyboard() if keyboard else None
    )

def handle_callback(event, vk):
    user_id = event.object['message']['from_id']
    callback_data = event.object['data']
    if callback_data.startswith("оплатил"):
        _, _, tokens, amount = callback_data.split("-")
        send_message(vk, 14, f"Пользователь {user_id} купил {tokens} токенов за {amount} рублей.")
    elif callback_data == "начать-диалог":
        response = "Начинаем новый диалог. Задайте свой вопрос."
        response_length = 0
        models.update_dialog_history(user_id, '')
        send_message(vk, user_id, response)
    elif callback_data == "вернуться-назад":
        keyboard = get_keyboard()
        send_message(vk, user_id, "Выберите действие:", keyboard=keyboard)

def handle_message(vk, user_id, message_text, openai_api_key):
    user_info = models.get_user_info(user_id)
    _, _, requests, level, tokens = user_info

    if message_text.lower() == "профиль":
        response = f"Уровень: {level}\nЗапросов: {requests}\nТокены: {tokens}"
        response_length = 0
    elif message_text.lower() == "начать диалог" or message_text.lower() == "новый диалог":
        response = "Начинаем новый диалог. Задайте свой вопрос."
        response_length = 0
        models.update_dialog_history(user_id, '')
    elif message_text.lower() == "пополнить токены":
        handle_top_up_request(vk, user_id)
        response = None
        response_length = 0
    elif message_text in ["10 рублей", "50 рублей", "100 рублей", "500 рублей"]:
        amount = int(message_text.split(" ")[0])
        tokens = calculate_tokens(amount)
        response = f"За {amount} рублей вы получите {tokens} токенов.\n\n" \
                   f"Чтобы пополнить токены, переведите {amount} рублей на QIWI номер +79999999999 и " \
                   f"укажите в описании к платежу ссылку на вашу страницу ВКонтакте."
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("Оплатил", color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button("Вернуться", color=VkKeyboardColor.POSITIVE)
        send_message(vk, user_id, response, keyboard=keyboard)
        response = None
        response_length = 0
    elif tokens >= 200:
        requests += 1
        dialog_history = models.get_dialog_history(user_id)
        prompt = f"{dialog_history}\nUser: {message_text}\nAssistant:"
        response, response_length = get_gpt_response(openai_api_key, prompt)
        tokens_spent = response_length * 4
        tokens -= tokens_spent
        models.update_user_tokens(user_id, tokens)
        update_user_level_and_requests(user_id, requests, level)
        models.update_dialog_history(user_id, f"{dialog_history}\nUser: {message_text}\nAssistant: {response}")
    else:
        response = "Недостаточно токенов для выполнения запроса"
        response_length = 0

    return response, response_length

def calculate_tokens(amount):
    tokens_per_ruble = 1000

    return amount * tokens_per_ruble

def handle_top_up_request(vk, user_id):
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button("10 рублей", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("50 рублей", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("100 рублей", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("500 рублей", color=VkKeyboardColor.PRIMARY)

    send_message(vk, user_id, "Выберите сумму пополнения:", keyboard=keyboard)

def update_user_level_and_requests(user_id, requests, level):
    new_level = determine_user_level(requests)

    if new_level != level:
        level = new_level
        models.update_user_level(user_id, level)

    models.update_user_requests(user_id, requests)

def determine_user_level(requests):
    if requests <= 150:
        return "Новичок"
    elif requests <= 500:
        return "Местный"
    elif requests <= 1000:
        return "Знающий"
    elif requests <= 1700:
        return "Сверхразум"
    else:
        return "Искусственный интеллект"

def get_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Новый диалог", color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("Профиль", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Пополнить токены", color=VkKeyboardColor.PRIMARY)
    return keyboard

