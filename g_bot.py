import telebot
from token_str import token
import g_sqlA as dbc
from g_bot_msg_lib import msg_text as mt

def main():
    
    db_str = 'sqlite:///sqlite3.db'
    db_con = dbc.DBclass(db_str)

    lang = 'en'

    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start(msg) :
        print(msg.from_user.id, msg.from_user.username, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.language_code)
        bot.send_message(msg.chat.id, mt[lang]['str1'] % {'user_first_name' : msg.from_user.first_name})

    @bot.message_handler(commands=["help"])
    def help(msg) :
        bot.send_message(msg.chat.id, mt[lang]['help'])

    bot.polling(none_stop = True)

if __name__ == '__main__':
    main()