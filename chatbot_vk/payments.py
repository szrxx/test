import hashlib
import requests
import time
import db.models

FK_SHOP_ID = 'your_shop_id'
FK_SECRET_KEY = 'your_shop_secret_key'

FK_NOTIFICATION_URL = 'https://yourserver.com/your_endpoint'

def generate_payment_link(shop_id, amount, payment_id, notification_url):
    # Ваш код для создания ссылки на оплату





    # Создайте ссылку на оплату
    payment_link = generate_payment_link(FK_SHOP_ID, amount, payment_id, FK_NOTIFICATION_URL)
    return payment_link

def process_payment_notification(request_data):
    # Проверьте подпись уведомления
    if not validate_payment_signature(FK_SHOP_ID, FK_SECRET_KEY, request_data):
        return False

    # Получите данные платежа
    user_id, timestamp = request_data.get('m_orderid').split('-')
    user_id = int(user_id)
    amount = float(request_data.get('amount'))

    # Начислите токены пользователю в зависимости от суммы платежа
    tokens = calculate_tokens(amount)
    models.add_user_tokens(user_id, tokens)

    return True

def calculate_tokens(amount):
    if amount == 10:
        return 30000
    elif amount == 50:
        return 42000
    elif amount == 100:
        return 150000
    elif amount == 500:
        return 800000
    else:
        return 0
