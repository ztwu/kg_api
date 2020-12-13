# -*- coding: utf-8 -*-
# @Time    : 2020/9/11 14:00
# @Author  : ztwu4
# @Email   : ztwu4@iflytek.com
# @File    : main.py
# @Software: PyCharm

import threading
from mysql_util import DB

db = DB()

def test1(thread_name):
    sql = "select * from user"
    res = db.query_sql(sql,None)
    print("test1"+"==="+thread_name)
    print(res)

def test2(thread_name):
    sql = "select * from user"
    res = db.query_sql(sql, None)
    print("test2"+"==="+thread_name)
    print(res)

def test3(thread_name):
    sql = "select * from user"
    res = db.query_sql(sql, None)
    print("test3"+"==="+thread_name)
    print(res)

def test4(thread_name):
    sql = "select * from user"
    res = db.query_sql(sql, None)
    print("test4"+"==="+thread_name)
    print(res)

def db_test(thread_name):
    test1(thread_name)
    # test2(thread_name)
    # test3(thread_name)
    # test4(thread_name)
    print(thread_name)

if __name__ == "__main__":
    for i in range(10):
        thread = threading.Thread(target=db_test, args=(("Thread" + str(i) + ":"),))
        thread.setDaemon(False)
        thread.start()