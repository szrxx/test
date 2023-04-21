from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def create_vkpay_keyboard(amounts, payload):
    keyboard = VkKeyboard(one_time=True)

    for amount in amounts:
        keyboard.add_vkpay_button(
            hash=f"action=transfer-to-group&group_id=YOUR_GROUP_ID&aid=YOUR_APP_ID&amount={amount * 100}&payload={payload}",
            color=VkKeyboardColor.POSITIVE
        )
        keyboard.add_line()

    return keyboard

def handle_top_up_request(vk, user_id):
    amounts = [10, 50, 100, 500]
    payload = f"topup_{user_id}"

    keyboard = create_vkpay_keyboard(amounts, payload)

    vk.messages.send(
        user_id=user_id,
        message="Выберите сумму пополнения:",
        random_id=0,
        keyboard=keyboard.get_keyboard()
    )
