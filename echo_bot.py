import telebot
import requests
import config as cfg
import db_functions
import re
from markup import *


telebot.apihelper.SESSION_TIME_TO_LIVE = 5 * 60
bot = telebot.TeleBot(cfg.telegramBotAPI, parse_mode=None)
news_API = cfg.newsAPI


@bot.message_handler(commands=['start', 'menu'])
def bot_greeting(message):
    db_functions.register_user(message.from_user.id)
    bot.send_message(message.chat.id, "Приветствую!", reply_markup=gen_main_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == '/menu' or call.data == '/start':
        bot.send_message(call.message.chat.id, "Чем могу помочь?", reply_markup=gen_main_markup())
    elif call.data == '/news':
        bot.send_message(call.message.chat.id, "Чем могу помочь?", reply_markup=gen_news_markup())
    elif call.data == '/subscriptions':
        bot.send_message(call.message.chat.id, "Выберите: ", reply_markup=gen_subscriptions_markup())
    elif call.data == '/get_news':
        bot.send_message(call.message.chat.id, "Выберите категорию новостей: ", reply_markup=gen_get_news_markup(call.from_user.id))
    elif call.data == '/my_subscriptions':
        subs = 'Категории на которые вы подписаны: \n\n'
        for item in db_functions.user_subscribes(call.from_user.id):
            subs += f'{categories[item[1]]} \n'
        bot.send_message(call.message.chat.id, f'{subs}', reply_markup=gen_subscriptions_markup())
    elif call.data == '/subscribe':
        bot.send_message(call.message.chat.id, "Выберите категорию для подписки: ", reply_markup=gen_subscribe_markup(call.from_user.id))
    elif call.data == '/unsubscribe':
        bot.send_message(call.message.chat.id, "Выберите категорию чтобы отписаться: ", reply_markup=gen_unsubscribe_markup(call.from_user.id))
    elif re.search(r'(\/news_)', call.data):
        category = str(call.data).split('_')[1].strip()
        a = requests.get(
            f'https://newsapi.org/v2/top-headlines?apiKey={news_API}&category={category}&pageSize=10&country=ru')
        for item in a.json()['articles']:
            bot.send_message(call.message.chat.id, f'{item["title"]} \n {item["publishedAt"]} \n {item["url"]} \n\n')
        bot.send_message(call.message.chat.id, 'Чем могу помочь?', reply_markup=gen_main_markup())
    elif re.search(r'(\/sub_)', call.data):
        user_id = call.from_user.id
        category = str(call.data).split('_')[1].strip()
        category_id = db_functions.find_category(category)[0]
        if not db_functions.user_subscribed(user_id, category_id):
            db_functions.subscribe(user_id, category_id)
            bot.send_message(call.message.chat.id, f'Вы успешно подписались на категорию \"{categories[category]}\"', reply_markup=gen_subscriptions_markup())
        else:
            bot.send_message(call.message.chat.id, f'Вы уже подписаны на \"{categories[category]}\"', reply_markup=gen_subscriptions_markup())

    elif re.search(r'(\/unsub_)', call.data):
        user_id = call.from_user.id
        category = str(call.data).split('_')[1].strip()
        category_id = db_functions.find_category(category)[0]
        if db_functions.user_subscribed(user_id, category_id):
            db_functions.unsubscribe(user_id, category_id)
            bot.send_message(call.message.chat.id, f'Вы успешно отписались от категории \"{categories[category]}\"', reply_markup=gen_subscriptions_markup())


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(message.chat.id, "Я не понимаю. Воспользуйтесь кнопками: ", reply_markup=gen_main_markup())









