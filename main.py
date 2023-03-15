import sqlite3
import pygetwindow as pg
import time
import json
import db


def start():
    try:
        con = sqlite3.connect("look.db")
        cur = con.cursor()
        result = cur.execute('SELECT * FROM messages LIMIT 1')
        con.close()
    except:
        con = sqlite3.connect("look.db")
        cur = con.cursor()
        result = cur.execute("""CREATE TABLE messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT ,
        datetime TEXT,
        status INTEGER)
        """)
        con.commit()
        result2 = cur.execute("""CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT ,
        password TEXT,
        name TEXT,
        user_id_message TEXT,
        status_to_send INTEGER)
        """)
        con.commit()
        result = cur.execute("""INSERT INTO users (id, login, password, name, user_id_message, status_to_send)
                                            VALUES(1, 'admin', '12345', 'Admin',Null, 0)""")
        con.commit()
        con.close()


def tracker():
    while True:
        title_old = pg.getAllTitles()
        time.sleep(1)
        title_new = pg.getAllTitles()
        if title_old[1] != title_new[1] and title_new[1] != "":
            data = {
                'message': title_new[1]
            }
            data = json.dumps(data)
            db.save_message(data)


if __name__ == '__main__':
    start()
    tracker()
