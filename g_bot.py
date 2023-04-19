import telebot
from token_str import token
import g_sqlA as dbc
from g_sqlA import User
from g_bot_msg_lib import msg_text as mt

def main():

    def replace_none(in_str, new_str):
        if in_str == None :
            return new_str
        else :
            return in_str


    lang = 'en'
    dbc.db_init()

    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start(msg) :
        print('call /start')
        print(msg.from_user.id, msg.from_user.username, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.language_code)
        dbc.sb_session_open()
        print(dbc.session.query(User).filter(User.tg_id == msg.from_user.id).count())
        if dbc.session.query(User).filter(User.tg_id == msg.from_user.id).count() > 0 :
            bot.send_message(msg.chat.id, mt[lang]['str2'] % {'user_first_name' : msg.from_user.first_name})
        else :
            new_user = User(
                tg_id = msg.from_user.id,
                username = replace_none(msg.from_user.username, str(msg.from_user.id)),
                last_name = replace_none(msg.from_user.last_name, str(msg.from_user.id)),
                first_name = replace_none(msg.from_user.first_name, str(msg.from_user.id)),
                language_code = replace_none(msg.from_user.language_code, str(msg.from_user.id))
            )
            dbc.session.add(new_user)
            dbc.session.commit()
            bot.send_message(msg.chat.id, mt[lang]['str1'] % {'user_first_name' : msg.from_user.first_name})


    @bot.message_handler(commands=["add"])
    def add(msg):
        print('call /start')

    

    






    @bot.message_handler(commands=["help"])
    def help(msg) :
        print('call /help')
        bot.send_message(msg.chat.id, mt[lang]['help'])




    @bot.message_handler(content_types=["text"])
    def unk(msg):
        bot.send_message(msg.chat.id, mt[lang]['unk1'])

    bot.polling(none_stop = True)

if __name__ == '__main__':
    main()