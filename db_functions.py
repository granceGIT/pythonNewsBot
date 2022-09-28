import sqlite3 as sql
from config import categories


def db_connect():
    with sql.connect('newsbot_db.db') as db:
        return db


def categories_insert():
    db = db_connect()
    cursor = db.cursor()
    for i in categories.keys():
        cursor.execute('INSERT INTO category (name) VALUES(?)', (i,))
        db.commit()


def categories_all():
    db = db_connect()
    return db.cursor().execute('SELECT * FROM category').fetchall()


def find_category(name):
    return db_connect().cursor().execute('SELECT * FROM category WHERE name=?', (name,)).fetchone()


def find_user(user_id):
    db = db_connect()
    cursor = db.cursor()
    return cursor.execute('SELECT * FROM users WHERE id=?', (user_id,)).fetchone()


def register_user(user_id):
    if not find_user(user_id):
        db = db_connect()
        cursor = db.cursor()
        cursor.execute('INSERT INTO users (id) VALUES(?)', (user_id,))
        db.commit()


def subscribe(user_id, category_id):
    if category_id > 0 and (category_id <= len(categories_all())):
        db = db_connect()
        cursor = db.cursor()
        cursor.execute("INSERT INTO subscribes (user_id,category_id) values (?,?)", (user_id, category_id,))
        db.commit()


def unsubscribe(user_id, category_id):
    user_subs = map(lambda item: item[0],user_subscribes(user_id))
    if category_id in user_subs:
        db = db_connect()
        cursor = db.cursor()
        cursor.execute("DELETE FROM subscribes WHERE user_id=? and category_id=?", (user_id, category_id,))
        db.commit()


def user_subscribes(user_id):
    db = db_connect()
    return db.cursor().execute("SELECT subscribes.category_id,category.name FROM subscribes,category "
                               "WHERE subscribes.user_id=? and category.id=subscribes.category_id", (user_id,)).fetchall()


def user_subscribed(user_id, category_id):
    db = db_connect()
    return bool(db.cursor().execute("SELECT * FROM subscribes WHERE user_id=? and category_id=?", (user_id, category_id,)).fetchone())
