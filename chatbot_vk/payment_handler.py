import hashlib
import requests

def validate_payment_signature(merchant_id, secret_key, request_data):
    sign = request_data.get("sign")

    if not sign:
        return False

    sorted_params = ":".join([
        merchant_id,
        request_data.get("amount", ""),
        request_data.get("intid", ""),
        request_data.get("m_curr", ""),
        request_data.get("m_orderid", ""),
        secret_key
    ])

    calculated_signature = hashlib.md5(sorted_params.encode()).hexdigest()

    return calculated_signature == sign

def create_payment_link(shop_id, payment_amount, payment_label, notification_url):
    payment_url = "https://frikassa.com/api"

    payment_data = {
        "m": shop_id,
        "oa": payment_amount,
        "o": payment_label,
        "s": hashlib.md5(f"{shop_id}:{payment_amount}:{notification_url}".encode()).hexdigest(),
        "lang": "ru",
        "i": "RUB",
        "em": "chatgptbot@example.com",
        "notification_url": notification_url
    }

    response = requests.post(payment_url, data=payment_data)

    if response.status_code == 200:
        return response.url
    else:
        return None
