from .database import create_connection

def get_user_info(user_id):
    conn = create_connection("chatbot_vk.sqlite")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cur.fetchone()

    if user is None:
        cur.execute("INSERT INTO users (user_id, requests, level, tokens) VALUES (?, 0, 'Новичок', 10000)", (user_id,))
        conn.commit()
        cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        user = cur.fetchone()

    conn.close()
    return user

def is_new_user(user_id):
    user = get_user_info(user_id)
    if user:
        _, requests, _, _, _ = user
        return requests == 0
    return False


def get_dialog_history(user_id):
    conn = create_connection("chatbot_vk.sqlite")
    cur = conn.cursor()
    cur.execute("SELECT history FROM dialogs WHERE user_id=?", (user_id,))
    history = cur.fetchone()

    if history is None:
        cur.execute("INSERT INTO dialogs (user_id, history) VALUES (?, '')", (user_id,))
        conn.commit()
        history = ''

    conn.close()
    return history

def update_dialog_history(user_id, new_history):
    conn = create_connection("chatbot_vk.sqlite")
    cur = conn.cursor()
    cur.execute("UPDATE dialogs SET history=? WHERE user_id=?", (new_history, user_id))
    conn.commit()
    conn.close()

def update_user_requests(user_id, requests):
    conn = create_connection("chatbot_vk.sqlite")
    cur = conn.cursor()
    cur.execute("UPDATE users SET requests=? WHERE user_id=?", (requests, user_id))
    conn.commit()
    conn.close()

def update_user_level(user_id, level):
    conn = create_connection("chatbot_vk.sqlite")
    cur = conn.cursor()
    cur.execute("UPDATE users SET level=? WHERE user_id=?", (level, user_id))
    conn.commit()
    conn.close()

def update_user_tokens(user_id, tokens):
    conn = create_connection("chatbot_vk.sqlite")
    cur = conn.cursor()
    cur.execute("UPDATE users SET tokens=? WHERE user_id=?", (tokens, user_id))
    conn.commit()
    conn.close()
