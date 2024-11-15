import json
import sqlite3
from loaderof_db import users_db
def create_users_db():
    conn = sqlite3.connect(users_db)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        users_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        phone_number NOT NULL,
                        card_number DEFAULT NULL,
                        event_list TEXT
                     )''')
    conn.commit()
    conn.close()


def user_register(username, phone_number, card_number=None):
    conn = sqlite3.connect(users_db)
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO users (username, phone_number, card_number, event_list)
                          VALUES (?, ?, ?, ?, ?)''', (username, phone_number, card_number, []))
        conn.commit()
        print("User registered successfully.")
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
    finally:
        conn.close()



def get_event_list(user_id):
    conn = sqlite3.connect(users_db)
    cursor = conn.cursor()
    cursor.execute('''SELECT event_list FROM users WHERE user_id = ?''', (user_id))
    event_list = cursor.fetchone()
    conn.close()
    return event_list


def add_event(user_id, new_event):

    event_list = json.loads(get_event_list(user_id))
    event_list.append(new_event)

    conn = sqlite3.connect(users_db)
    cursor = conn.cursor()
    cursor.execute('''UPDATE event SET event_list = ? WHERE user_id = ?''', (event_list, user_id))
    conn.commit()
    conn.close()

create_users_db()


def take_id_by_phonenumber(phonenumber):
    conn = sqlite3.connect(phonenumber)
    cursor = conn.cursor()
    cursor.execute('''SELECT id FROM Events WHERE users_id = ?''', (phonenumber))
    q = cursor.fetchone()
    conn.commit()
    conn.close()
    return q


def user_login(username):
    conn = sqlite3.connect(users_db)
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT username FROM users WHERE username = ?''', (username))
    except Exception:
        return "Пользователь с таким ником уже существует"
    conn.close()

create_users_db()
