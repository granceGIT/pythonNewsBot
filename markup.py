from telebot.types import InlineKeyboardMarkup as ikm,InlineKeyboardButton as ikb
from db_functions import user_subscribes
from config import categories


def gen_main_markup():
    markup = ikm()
    markup.row_width = 2
    markup.add(ikb('Новости', callback_data='/news'),
               ikb('Подписки', callback_data='/subscriptions'))
    return markup


def gen_news_markup():
    markup = ikm()
    markup.row_width = 2
    markup.add(ikb('Получить новости', callback_data='/get_news'),
               ikb('На главную', callback_data='/menu'))
    return markup


def gen_get_news_markup(user_id):
    markup = ikm()
    markup.row_width = 3
    for subscribe in user_subscribes(user_id):
        category = subscribe[1]
        markup.add(
            ikb(f'{categories[category]}', callback_data=f'/news_{category}')
        )
    markup.add(ikb('Назад', callback_data='/news'))
    return markup


def gen_subscriptions_markup():
    markup = ikm()
    markup.row_width = 3
    markup.add(
        ikb('Мои подписки', callback_data='/my_subscriptions'),
        ikb('Подписаться', callback_data='/subscribe'),
        ikb('Отписаться', callback_data='/unsubscribe'),
        ikb('Назад', callback_data='/menu'),
    )

    return markup


def gen_unsubscribe_markup(user_id):
    markup = ikm()
    markup.row_width = 3
    for subscribe in user_subscribes(user_id):
        category = subscribe[1]
        markup.add(
            ikb(f'{categories[category]}', callback_data=f'/unsub_{category}')
        )
    markup.add(ikb('Назад', callback_data='/subscriptions'))
    return markup


def gen_subscribe_markup(user_id):
    markup = ikm()
    markup.row_width = 3
    for key in categories:
        markup.add(ikb(f'{categories[key]}', callback_data=f'/sub_{key.strip()}'))
    markup.add(ikb('Назад', callback_data='/subscriptions'))
    return markup
