import mysql.connector
from mysql.connector import Error
import tkinter
from tkinter import messagebox


def init_db():
    return mysql.connector.connect(
                    host='b7fc6ph1k1gdekallipl-mysql.services.clever-cloud.com',
                    database='b7fc6ph1k1gdekallipl',
                    user='uyzkm56s2zsfqhle',
                    password='GgwFP3YTyAnMMfFj9gPL'
                )
                
connection = mysql.connector.connect(
                    host='b7fc6ph1k1gdekallipl-mysql.services.clever-cloud.com',
                    database='b7fc6ph1k1gdekallipl',
                    user='uyzkm56s2zsfqhle',
                    password='GgwFP3YTyAnMMfFj9gPL'
                )

def sql_select(query):
    print(query)
    global connection
    try:
        connection.ping(reconnect=True, attempts=3, delay=5)
    except mysql.connector.Error as err:
        connection = init_db()

    cursor = connection.cursor()

    cursor.execute(query)
    return cursor.fetchall()

def sql(query):
    print(query)
    global connection
    try:
        connection.ping(reconnect=True, attempts=3, delay=5)
    except mysql.connector.Error as err:
        connection = init_db()

    cursor = connection.cursor()
    # try:
    #     cursor.execute(query)
    #     connection.commit()
    # except Exception as e:
    #     print("Exception: ", e)

    cursor.execute(query)
    connection.commit()

def sql_items(query, items):
    print(query, items)

    global connection
    try:
        connection.ping(reconnect=True, attempts=3, delay=5)
    except mysql.connector.Error as err:
        connection = init_db()

    cursor = connection.cursor()

    cursor.execute(query, list(items))
    connection.commit()

def sql_items_select(query, items):
    print(query, items)

    global connection
    try:
        connection.ping(reconnect=True, attempts=3, delay=5)
    except mysql.connector.Error as err:
        connection = init_db()

    cursor = connection.cursor()

    cursor.execute(query, list(items))
    return cursor.fetchall()

