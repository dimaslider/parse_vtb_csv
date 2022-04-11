'''
взято с https://kee-reel.com/python-web-server-ru
'''
from flask import Flask, render_template, request
from datetime import datetime
import sqlite3

app = Flask('my_first_server')
DB_NAME = 'messages.db'

def init_wall_data():
    '''
    Открываем соединение с базой. Если файла базы ещё нет, то он создастся.
    Создаём таблицу с названием wall. Если она уже создана, то ничего не делаем.
    В этой таблице есть:
    - численный id, уникальный для каждой записи
    - строка nick - тут будет ник пользователя
    - строка message - тут будет сообщение, которое он оставил
    '''
    conn = sqlite3.connect(DB_NAME)
    conn.execute('''create table if not exists wall (
            id INTEGER PRIMARY KEY,
            nick TEXT,
            message TEXT)''')
    # Эта строчка сохраняет внесённые изменения -- она нужна при
    # создании таблиц и при добавлении/обновлении/удалении полей
    conn.commit()

def set_wall_data(nick, message):
    '''
    Записываем новое сообщение в таблицу wall
    '''
    conn = sqlite3.connect(DB_NAME)
    conn.execute('insert into wall(nick, message) values(?, ?)', (nick, message))
    conn.commit()

def get_wall_data():
    '''
    Забираем все записи из таблицы wall
    '''
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute('select nick, message from wall')
    rows = cursor.fetchall()
    return rows

def render_main_page():
    '''
    Отдельная функция, которая подставляет в шаблон все необходимые значения
    '''
    cur_datetime_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    wall_data = get_wall_data()
    return render_template("index_db.html", cur_datetime=cur_datetime_str,
            len=len(wall_data), wall_data=wall_data)

@app.route('/wall', methods=['POST'])
def response():
    '''
    Обработчик, который принимает данные от пользователя,
    вставляет их в базу и возвращает обновлённую страничку
    '''
    nick = request.form.get("nick")
    message = request.form.get("message")
    set_wall_data(nick, message)
    return render_main_page()

@app.route('/')
def handle_time():
    return render_main_page()

init_wall_data()
 
app.run(port=9000)