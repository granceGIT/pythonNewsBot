import echo_bot
from create_db import create_db


def init_bot(bot):
    bot.polling()


if __name__ == '__main__':
    print('Bot polling...')
    create_db()
    init_bot(echo_bot.bot)
