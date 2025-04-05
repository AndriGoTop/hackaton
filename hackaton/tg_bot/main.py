import sqlite3
import re
from datetime import datetime, timedelta
import telebot
import os
from time import sleep

script_dir_db = os.path.dirname(os.path.abspath(__file__))
file_path_db = os.path.join(script_dir_db, 'db.sqlite3').split('/')
file_path_db.pop(-2)
file_path_db = '/'.join(file_path_db)
connection = sqlite3.connect(file_path_db)
cursor = connection.cursor()
token="7507400371:AAH35AhIdwdYcc2pxjgr6w8f2Hssmk-94ZQ"
bot=telebot.TeleBot(token)

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
        print(1)
        cursor.execute('BEGIN;')
        print(2)
        cursor.execute(f"INSERT INTO users_tg (tg_id, tg_link) VALUES ('{data[0]['id_user']}', '@{data[0]['link']}');")
        print(3)
        cursor.execute('COMMIT;')
    except:
        print(4)
        cursor.execute('ROLLBACK;')
    connection.close()

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'users.sqlite3')
connection = sqlite3.connect(file_path)
cursor = connection.cursor()
cursor.execute('SELECT tg_id FROM users_tg;')
results = cursor.fetchall()
print(results)
connection.close()

def check_updates():
    cursor.execute('''
    SELECT updated_at FROM apphub_customuser;
    ''')
    results = cursor.fetchall()
    for i in results:
        date_f = re.split('[-, :]', i[0])
        date_r = [int(float(i)) for i in date_f]
        date_time = datetime(date_r[0], date_r[1], date_r[2], date_r[3], date_r[4])
        if datetime.today() < date_time + timedelta(minutes=5):
            bot.send_message('', '')
    connection.close()

while True:
    print('Обновление', datetime.today())
    check_updates()
    sleep(300)

bot.polling(none_stop=True)