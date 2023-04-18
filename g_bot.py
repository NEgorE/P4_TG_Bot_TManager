import telebot

from token_str import token
bot = telebot.TeleBot(token)

from g_bot_msg_lib import msg_text as mt
lang = 'en'

@bot.message_handler(commands=["start"])
def start(msg) :
    print(msg.from_user.id, msg.from_user.username, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.language_code)
    bot.send_message(msg.chat.id, mt[lang]['str1'] % {'user_first_name' : msg.from_user.first_name})





bot.polling(none_stop = True)