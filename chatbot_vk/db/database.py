import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def create_users_table(conn):
    user_table = """CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER NOT NULL UNIQUE,
                        requests INTEGER,
                        level TEXT,
                        tokens INTEGER DEFAULT 3000
                    );"""
    create_table(conn, user_table)

def create_dialogs_table(conn):
    dialogs_table = """CREATE TABLE IF NOT EXISTS dialogs (
                           user_id INTEGER PRIMARY KEY,
                           history TEXT NOT NULL
                       );"""
    create_table(conn, dialogs_table)

def initialize_database():
    database = "chatbot_vk.sqlite"

    conn = create_connection(database)

    if conn is not None:
        create_users_table(conn)
        create_dialogs_table(conn)
        conn.commit()
        conn.close()
    else:
        print("Error! Cannot create the database connection.")
