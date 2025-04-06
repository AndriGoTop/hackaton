import sqlite3
import re
from datetime import datetime, timedelta
import telebot
import os
from time import sleep

# Подключение бота
token="7507400371:AAH35AhIdwdYcc2pxjgr6w8f2Hssmk-94ZQ"
bot=telebot.TeleBot(token)

# Бот отправляет принимает данные о пользователле при /start
@bot.message_handler(commands=['start'])
def start(message):
    data = [{
        'link': message.from_user.username,
        'id_user': message.from_user.id,
    }]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'users.sqlite3')
    connection = sqlite3.connect(file_path)
    cursor = connection.cursor()
    try:
        cursor.execute('BEGIN;')
        cursor.execute(f"INSERT INTO users_tg (tg_id, tg_link) VALUES ('{data[0]['id_user']}', '@{data[0]['link']}');")
        cursor.execute('COMMIT;')
    except:
        cursor.execute('ROLLBACK;')
    connection.close()

# Проверяет как давно обновлялась подборка у пользователей
def check_updates():
    script_dir_db = os.path.dirname(os.path.abspath(__file__))
    file_path_db = os.path.join(script_dir_db, 'db.sqlite3').split('/')
    file_path_db.pop(-2)
    file_path_db = '/'.join(file_path_db)
    connection = sqlite3.connect(file_path_db)
    cursor = connection.cursor()
    cursor.execute('SELECT updated_at FROM apphub_customuser;')
    results = cursor.fetchall()

    script_dir_db_s = os.path.dirname(os.path.abspath(__file__))
    file_path_db_s = os.path.join(script_dir_db_s, 'users.sqlite3')
    script_dir_s = os.path.dirname(os.path.abspath(__file__))
    file_path_s = os.path.join(script_dir_s, 'users.sqlite3')
    connection_s= sqlite3.connect(file_path_s)
    cursor_s = connection_s.cursor()
    for updated_at_s in results:
        date_f = re.split('[-, :]', updated_at_s[0])
        date_r = [int(float(i)) for i in date_f]
        date_time = datetime(date_r[0], date_r[1], date_r[2], date_r[3], date_r[4])
        print(date_time + timedelta(minutes=5))
        if datetime.today() < date_time + timedelta(hours=3, minutes=5):
            cursor.execute('''SELECT apphub_subs.sub
                        FROM apphub_subs
                        JOIN apphub_customuser ON apphub_subs.id = apphub_customuser.telegram_id_id''')
            subs = cursor.fetchall()
            for i in subs:
                try:
                    user_link = i[0]
                    print(user_link)
                    cursor_s.execute(f'''
                        SELECT tg_id FROM users_tg
                                                WHERE tg_link == "{user_link}";
                    ''')
                    chat_id = cursor_s.fetchall()
                    print(updated_at_s[0])
                    cursor.execute(f'SELECT username FROM apphub_customuser WHERE updated_at == "{updated_at_s[0]}";')
                    name = cursor.fetchall()
                    bot.send_message(chat_id[0][0], f'{name[0][0]} изменил свою подборку')
                except:
                    pass

    connection.close()
    connection_s.close()

check_updates()

# while True:
#     print('Обновление', datetime.today())
#     # check_updates()
#     sleep(300)

bot.polling(none_stop=True)
