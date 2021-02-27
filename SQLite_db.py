import sqlite3


def connect_db():
    """ Подключаемся к БД и сохраняем курсор соединения """
    connection = sqlite3.connect("base.db")
    cursor = connection.cursor()

    """ Создание таблицы, если ее нет (IF NOT EXISTS) """
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                    user_id INTEGER,
                    rub FLOAT,
                    status TEXT
                    )""")
    connection.commit()
    return {"connection": connection, "cursor": cursor}


def add_user(user_id, rub, status):
    """ Добавляем нового пользователя """
    db = connect_db()
    cursor = db["cursor"]
    connection = db["connection"]

    cursor.execute(f"INSERT INTO users VALUES(?, ?, ?)", (int(user_id), int(rub), status))
    connection.commit()


def user_exists(user_id):
    """ Проверяем, есть ли уже юзер в базе """
    cursor = connect_db()["cursor"]

    cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
    if cursor.fetchone() is None:
        return False
    else:
        return True


def change_user_rub(user_id, rub):
    """ Для редактирования rub пользователя """
    db = connect_db()
    cursor = db["cursor"]
    connection = db["connection"]

    cursor.execute(f"UPDATE users SET rub = '{rub}' WHERE user_id = '{user_id}'")
    connection.commit()


def change_userstatus(user_id, status):
    """ Для редактирования статуса пользователя """
    db = connect_db()
    cursor = db["cursor"]
    connection = db["connection"]

    cursor.execute(f"UPDATE users SET status = '{status}' WHERE user_id = '{user_id}'")
    connection.commit()


def check_userinfo(user_id):
    """ Выводит информацию пользователя """
    cursor = connect_db()["cursor"]

    for value in cursor.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'"):
        return {"user_id": value[0],
                "rub": value[1],
                "status": value[2]
                }


def close():
    """Закрываем соединение с БД"""
    connection = connect_db()["connection"]
    connection.close()
