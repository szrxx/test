import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import time
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from core.message_handler import send_message, handle_message, get_keyboard
from db.database import initialize_database
from db import models

# Замените данными своего приложения и токена
VK_GROUP_TOKEN = 'vk1.a.okHh8BLpUGTFIZUKHepft8ZWpNl3z6CTNS5YeLxXChZzEzSGOZH7CZ9HcMJ0fJEfok-yCynQGV5alM0UpDNrh8v-xrFyenpav5qmmecX3xDoKL_mVtd8-QVlJ-gBlfLgtm_eC5wAgW-HRK9y2944sj2WASZI4FqbidZu97p0Pr-nlkSuAP_iqDsUj94Rbwf2o7_Lyurf_GD_ola6zs2XkQ'
OPENAI_API_KEY = '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'

def get_welcome_keyboard():
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button("Подписаться на группу", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("Правила использования", color=VkKeyboardColor.POSITIVE)

    return keyboard.get_keyboard()

ADMIN_IDS = [749818345, 586865983]  # Замените на ID администраторов

def add_tokens(user_id, tokens_amount):
    user_info = models.get_user_info(user_id)
    current_tokens = user_info[4]  # Исправлено здесь
    new_tokens = current_tokens + tokens_amount
    models.update_user_tokens(user_id, new_tokens)



def main():
    initialize_database()

    vk_session = vk_api.VkApi(token=VK_GROUP_TOKEN, api_version='5.131')
    vk = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    print("Бот запущен. Ожидание сообщений...")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            message_text = event.text

            print(f"Получено сообщение от {user_id}: {message_text}")

            if models.is_new_user(user_id):
                welcome_message = "Привет, я бот ChatGPT! Вот некоторые полезные ссылки:"
                welcome_keyboard = get_welcome_keyboard()
                send_message(vk, user_id, welcome_message, keyboard=welcome_keyboard)

            if user_id in ADMIN_IDS and message_text.startswith("/get "):
                try:
                    target_user_id, tokens_amount = map(int, message_text.split()[1:3])
                    add_tokens(target_user_id, tokens_amount)
                    send_message(vk, user_id, f"Выдано {tokens_amount} токенов пользователю с ID {target_user_id}.")
                    continue
                except ValueError:
                    send_message(vk, user_id, "Неверный формат команды. Используйте: /get id_user количество_токенов")
                    continue

            user_info = models.get_user_info(user_id)
            _, _, _, history, tokens = user_info

            # Проверка длины истории и очистка, если превышает 4000 символов
            if len(history) > 4000:
                models.update_dialog_history(user_id, "")
                send_message(vk, user_id, "Диалог достиг максимального количества символов. Начат новый диалог.")
                continue

            response, response_length = handle_message(vk, user_id, message_text, OPENAI_API_KEY)
            print(f"Ответ GPT: {response}")

            keyboard = get_keyboard()

            if response != "Недостаточно токенов для выполнения запроса":
                if response is not None:
                    send_message(vk, user_id, response, keyboard=keyboard)

                if message_text.lower() not in ["профиль", "новый диалог", "пополнить токены", "10 рублей", "50 рублей", "100 рублей", "500 рублей"]:
                    time.sleep(1)
                    spent_tokens = response_length * 4
                    remaining_tokens = tokens - spent_tokens
                    send_message(vk, user_id, f"Списано {spent_tokens} токенов. Осталось {remaining_tokens} токенов", keyboard=keyboard)
                    
                    # Обновление истории
                    new_history = history + f"\n{message_text}\n{response}"
                    models.update_dialog_history(user_id, new_history)
            else:
                send_message(vk, user_id, response, keyboard=keyboard)

            if message_text == "Оплатил":
                my_user_id = 749818345
                send_message(vk, user_id, "Запрос на пополнение токенов получен. Токены будут начислены в течение 10 минут.")

                vk.messages.send(user_id=my_user_id, message=f"Пользователь {user_id} купил токены.", random_id=random.randint(1, 2 ** 31))

            elif message_text.lower() == "вернуться назад":
                response, response_length = handle_message(vk, user_id, "новый диалог", OPENAI_API_KEY)
                if response is not None:
                    send_message(vk, user_id, response, keyboard=keyboard)






if __name__ == "__main__":
    main()



