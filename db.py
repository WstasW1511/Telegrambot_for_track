import datetime
import sqlite3
import json


def result_sql_user(result):
    results = []
    for i in result:
        result = {}
        result['id'] = i[0]
        result['login'] = i[1]
        result['password'] = i[2]
        result['name'] = i[3]
        results.append(result)
    return results


def result_sql(result):
    results = []
    for i in result:
        result = {}
        result['id'] = i[0]
        result['message'] = i[1]
        result['datetime'] = i[2]
        results.append(result)
    return results


def update_status(id):
    try:
        con = sqlite3.connect('look.db')
        cur = con.cursor()
        query = """update messages set status=%s where id=%s""" % (1, id)
        result = cur.execute(query)
        con.commit()
        con.close()
    except Exception as e:
        print(e)


def get_message_for_send(user_id_message):
    try:
        con = sqlite3.connect("look.db")
        cur = con.cursor()
        stat = cur.execute('SELECT status_to_send FROM "users" WHERE user_id_message =%s'% user_id_message)
        stat = stat.fetchall()
        stat = stat[0][0]
        if stat != 1:
            result = cur.execute('SELECT * FROM "messages" where status = 0 ORDER BY datetime LIMIT 1 ')
            res = result.fetchall()
            result = result_sql(res)
            con.close()
            if result != []:
                data = {
                    'id': result[0]['id'],
                    'message': result[0]['message'],
                    'datetime': result[0]['datetime']
                        }
                update_status(data['id'])
        else:
            data = "no"
        data = json.dumps(data)
        return data

    except Exception as e:
        print(e)


def save_message(message):
    message = json.loads(message)
    try:
        con = sqlite3.connect('look.db')
        cur = con.cursor()
        now = datetime.datetime.now()
        query = """INSERT INTO messages (message, datetime, status) 
        VALUES('%s', '%s', %s)"""%(message['message'], (now.strftime("(%H:%M:%S) %m/%d/%Y")), 0)
        result = cur.execute(query)
        con.commit()
        con.close()
    except Exception as e:
        print(e)


def insert_user_id(id, user_id_message):
    try:
        con = sqlite3.connect('look.db')
        cur = con.cursor()
        query = """update users set user_id_message=%s where id=%s""" % (user_id_message, id)
        result = cur.execute(query)
        con.commit()
        con.close()
    except Exception as e:
        print(e)


def login(request):
    data = json.loads(request)
    login = data['login'].lower()
    password = data['password']
    user_id_message = data['user_id_message']
    try:
        con = sqlite3.connect('look.db')
        cur = con.cursor()
        query = "select * from users where login='%s' and password='%s'"%(login, password)
        res = cur.execute(query)
        res = res.fetchall()
        result = result_sql_user(res)
        con.close()
        if result:
            insert_user_id(result[0]['id'], user_id_message)
            return json.dumps(result[0])
        else:
            return 'Не верный Логин или пароль.'
    except:
        print("Ошибка")


def status_to_send(user_id, status):
    if status:
        status = 0
    else:
        status = 1
    try:
        con = sqlite3.connect('look.db')
        cur = con.cursor()
        query = """update users set status_to_send=%s where user_id_message=%s""" % (status, user_id)
        result = cur.execute(query)
        con.commit()
        con.close()
    except Exception as e:
        print(e)
