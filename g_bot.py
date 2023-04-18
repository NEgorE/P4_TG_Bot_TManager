import telebot
from token_str import token
import g_sqlA as dbc
from g_sqlA import User
from g_bot_msg_lib import msg_text as mt

def main():

    lang = 'en'
    dbc.db_init()

    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start(msg) :
        print(msg.from_user.id, msg.from_user.username, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.language_code)
        bot.send_message(msg.chat.id, mt[lang]['str1'] % {'user_first_name' : msg.from_user.first_name})
        print(dbc.session.query(dbc.User).count())





    @bot.message_handler(commands=["help"])
    def help(msg) :
        bot.send_message(msg.chat.id, mt[lang]['help'])

    bot.polling(none_stop = True)

if __name__ == '__main__':
    main()