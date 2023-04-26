import telebot
import datetime
from token_str import token
import g_sqlA as dbc
from g_sqlA import User, Task, Sched_item
from sqlalchemy import func, desc
from g_bot_msg_lib import msg_text as mt

input_values = {}

def main():

    def replace_none(in_str, new_str):
        if in_str == None :
            return new_str
        else :
            return in_str

    
    date_format = '%Y-%m-%d'
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
            dbc.session.close()
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
    def add(msg, com = 'INIT'):
        global input_values
        print(f'User {msg.from_user.id} call /add whith \'{com}\' param')
        if com == 'INIT' :
            input_values = {}
            input_values['task_id'] = get_max_task_id() + 1
            input_values['task_user_id'] = msg.from_user.id
            bot.send_message(msg.chat.id, mt[lang]['add_str1'])
            bot.register_next_step_handler(msg, add, 'INPUT_DATE')
        elif com == 'INPUT_DATE' :
            in_date = check_date(msg)
            if in_date == '' :
                bot.register_next_step_handler(msg, add, 'INPUT_DATE')
            else :
                input_values['task_date'] = in_date
                bot.send_message(msg.chat.id, mt[lang]['add_str2'])
                bot.register_next_step_handler(msg, add, 'INPUT_TIME')   
        elif com in ['INPUT_TIME','INPUT_NOTIF_TIME'] :
            in_time = check_time(msg)
            if in_time == '' :
                if com == 'INPUT_TIME' :
                    bot.register_next_step_handler(msg, add, 'INPUT_TIME')
                else :
                    bot.register_next_step_handler(msg, add, 'INPUT_NOTIF_TIME')
            else :
                if com == 'INPUT_TIME' :
                    input_values['task_time'] = in_time
                    bot.send_message(msg.chat.id, mt[lang]['add_str3'])
                    bot.register_next_step_handler(msg, add, 'TASK_TEXT')
                else :
                    input_values['notif_time'] = in_time
                    input_values['task_status'] = 'ToDo'
                    save_task(msg.chat.id, input_values)
        elif com == 'TASK_TEXT' :
            in_task_text = msg.text
            if in_task_text == '' :
                bot.send_message(msg.chat.id, mt[lang]['add_str4'])
                bot.send_message(msg.chat.id, mt[lang]['add_str3'])
                bot.register_next_step_handler(msg, add, 'TASK_TEXT')
            else :
                input_values['task_text'] = in_task_text
                bot.send_message(msg.chat.id, mt[lang]['add_str5'])
                bot.register_next_step_handler(msg, add, 'NOTIF_NEED')
        elif com == 'NOTIF_NEED' :
            in_notif_need = msg.text
            if in_notif_need == 'Y' :
                input_values['notif_need'] = in_notif_need
                bot.send_message(msg.chat.id, mt[lang]['add_str6'])
                bot.register_next_step_handler(msg, add, 'INPUT_NOTIF_TIME')
            elif in_notif_need == 'N' :
                input_values['notif_need'] = in_notif_need
                input_values['task_status'] = 'ToDo'
                save_task(msg.chat.id, input_values)
            else :
                bot.send_message(msg.chat.id, mt[lang]['add_str7'])
                bot.send_message(msg.chat.id, mt[lang]['add_str5'])
                bot.register_next_step_handler(msg, add, 'NOTIF_NEED')
        
        print(input_values)
    

    @bot.message_handler(commands=["show"])
    def show(msg) :
        print(f'User {msg.from_user.id} call /show')
        dbc.sb_session_open()
        if msg.text == '/show' :
            res = dbc.session.query(Task).order_by(Task.created_dt , Task.time).limit(10).all()
            show_tasks(res, msg.chat.id)
        else :
            p_date_in = msg.text[msg.text.find(' ')+1:len(msg.text)]
            res = dbc.session.query(Task).filter(Task.date == p_date_in).order_by(Task.created_dt , Task.time).limit(10).all()
            show_tasks(res, msg.chat.id)
        dbc.session.close()
    

    def show_tasks(lfp, msg_id) :
        answ = ''
        cur_date = ''
        pref_date = ''
        for task in lfp :
            cur_date = task.date
            if cur_date != pref_date : 
                answ += f'\n{cur_date}:'
            out_time = task.time.strftime('%H:%M')
            answ += f'\n    - {out_time} : {task.text} (task ID: {task.id})'
            pref_date = cur_date
        answ += ''
        if len(answ.strip()) > 0 :
            bot.send_message(msg_id, answ)
        else :
            bot.send_message(msg_id, mt[lang]['str3'])


    def save_task(chat_id, in_dict) :
        new_task = Task(
            id = in_dict['task_id'],
            user_id = in_dict['task_user_id'],
            date = datetime.datetime.strptime(in_dict['task_date'], date_format),
            time = datetime.time.fromisoformat(in_dict['task_time'] + ':00'),
            text = in_dict['task_text'],
            status = in_dict['task_status']
        )
        dbc.sb_session_open()
        dbc.session.add(new_task)
        if in_dict['notif_need'] == 'Y' :
            new_s_item = Sched_item(
                task_id = in_dict['task_id'],
                time = datetime.time.fromisoformat(in_dict['notif_time'] + ':00')
            )
            dbc.session.add(new_s_item)
        
        dbc.session.commit()
        bot.send_message(chat_id, mt[lang]['add_str8'])
        print('Task saved!!!')


    def check_time(msg) :
        t_time_in = ''
        try :
            hh = int(msg.text[0:2])
            mm = int(msg.text[3:5])
            if hh < 25 and mm < 60  and msg.text[2] ==':':
                t_time_in = msg.text
            else :
                t_time_in = ''
        except ValueError:
            t_time_in = ''
        if t_time_in == '' :
            bot.send_message(msg.chat.id, mt[lang]['ch_t_str1'])
            bot.send_message(msg.chat.id, mt[lang]['add_str2'])
        return t_time_in


    def check_date(msg) :
        return_str = ''
        try:
            dateObject = datetime.datetime.strptime(msg.text, date_format)
            return_str = msg.text
        except ValueError:
            bot.send_message(msg.chat.id, mt[lang]['ch_d_str1'])
            bot.send_message(msg.chat.id, mt[lang]['add_str1'])
        return return_str


    def get_max_task_id():
        dbc.sb_session_open()
        ret_val = replace_none(dbc.session.query(func.max(Task.id))[0][0],0)
        dbc.session.close()
        return ret_val


    @bot.message_handler(commands=["help"])
    def help(msg) :
        print(f'User {msg.from_user.id} call /help')
        bot.send_message(msg.chat.id, mt[lang]['help'])


    @bot.message_handler(content_types=["text"])
    def unk(msg):
        print(f'User {msg.from_user.id} call {msg.text}')
        bot.send_message(msg.chat.id, mt[lang]['unk1'])


    bot.polling(none_stop = True)


if __name__ == '__main__':
    main()