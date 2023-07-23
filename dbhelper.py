import sqlite3
import mysql.connector

import utils as utls
import settings


USE_MYSQL_DB = True


def _mysql_create_db_if_not_exist():
    conn = mysql.connector.connect(
    host=settings.envvars.host,
    user=settings.envvars.user,
    password=settings.envvars.password)
    
    cur = conn.cursor()
    
    cur.execute("SHOW DATABASES")
    result = False
    for x in cur:
        if x[0] == settings.envvars.database_name:
            result = True
            break
        
    if result == False:
        cur.execute(f'CREATE DATABASE {settings.envvars.database_name}')
    
    cur.close()
    conn.close()
    
    return result



def _get_db_mysql():
    mydb = mysql.connector.connect(
        host=settings.envvars.host,
        user=settings.envvars.user,
        password=settings.envvars.password,
        database=settings.envvars.database_name)
    
    return mydb


def _get_db_sqlite():
    return sqlite3.connect(settings.envvars.database_file)



def get_db():
    if USE_MYSQL_DB: return _get_db_mysql()
    else: return _get_db_sqlite()


def setup():
    if USE_MYSQL_DB: _mysql_create_db_if_not_exist()
    
    conn = get_db()
    cur = conn.cursor()
    
    if USE_MYSQL_DB:
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS 
            posts(id INTEGER PRIMARY KEY AUTO_INCREMENT, 
            title TEXT NOT NULL, body TEXT NOT NULL)''')
        
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS 
            users(id INTEGER PRIMARY KEY AUTO_INCREMENT, 
            email VARCHAR(255) NOT NULL UNIQUE, password TEXT NOT NULL)''')
    else:
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS 
            posts(id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title TEXT NOT NULL, body TEXT NOT NULL)''')
        
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS 
            users(id INTEGER PRIMARY KEY AUTOINCREMENT, 
            email TEXT NOT NULL UNIQUE, password TEXT NOT NULL)''')
    
    conn.commit()
    
    cur.close()
    conn.close()






def new_user(email, password):
    conn = get_db()
    cur = conn.cursor()
    res = None

    password = utls.hash(password)

    try:
        cur.execute(
        '''INSERT INTO users(email, password) VALUES (%s, %s)''', (email, password))
    except sqlite3.IntegrityError:
        res = 'integrity error while inserting.'
    
    if not res:
        res = cur.lastrowid
    
    conn.commit()

    print('row id--------->',res)
    cur.close()
    conn.close()
    return res

def get_user(id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        '''SELECT * FROM users WHERE id = ?''', (str(id)))
    
    usr = cur.fetchone()

    cur.close()
    conn.close()
    return usr

def get_user_by_email(email):
    conn = get_db()
    cur = conn.cursor()
    #print(email,'-------', type(email))
    cur.execute(
        '''SELECT * FROM users WHERE email = ?''', (email,))
    
    usr = cur.fetchone()

    cur.close()
    conn.close()
    return usr

def new_post(title, body):
    conn = get_db()
    cur = conn.cursor()

    res = None
    try:
        cur.execute(
        '''INSERT INTO posts(title, body) VALUES (?, ?) RETURNING *''', (title, body))
    except sqlite3.IntegrityError:
        res = 'integrity error while inserting.'
    

    if not res: 
        res = cur.fetchone()
    
    conn.commit()

    

    cur.close()
    conn.close()
    return res

def get_posts():
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        '''SELECT * FROM posts''')
    
    posts = cur.fetchall()

    cur.close()
    conn.close()
    return posts

def get_post(id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        '''SELECT * FROM posts WHERE id = ?''', (str(id)))
    
    post = cur.fetchone()

    cur.close()
    conn.close()
    return post

def delete_post(id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        '''DELETE FROM posts WHERE id = ? RETURNING *''', (str(id)))
    
    post = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()
    return post

def update_post(id, title, body):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        '''UPDATE posts SET title = ?, body = ? WHERE id = ? RETURNING *''', 
        (title, body, str(id)))
    
    post = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()
    return post