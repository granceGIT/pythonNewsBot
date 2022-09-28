import sqlite3 as sql
from db_functions import categories_insert


def create_db():
    connect = sql.connect('newsbot_db.db')
    cursor = connect.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS "users" (
            "id"	INTEGER,
            PRIMARY KEY("id" AUTOINCREMENT)
        );''')
    connect.commit()

    cursor.execute(''' CREATE TABLE IF NOT EXISTS "category" (
    "id"	INTEGER NOT NULL,
    "name"	TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id" AUTOINCREMENT)); ''')
    connect.commit()

    cursor.execute(''' CREATE TABLE IF NOT EXISTS "subscribes" (
    "user_id"	INTEGER,
    "category_id"	INTEGER,
    CONSTRAINT `fkSubsUser` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
    CONSTRAINT `fkSubsCategory` FOREIGN KEY(`category_id`) REFERENCES `category`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
    ); ''')
    connect.commit()

    try:
        categories_insert()
    except:
        pass
