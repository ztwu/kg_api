# -*- coding: utf-8 -*-
# @Time    : 2020/9/11 13:51
# @Author  : ztwu4
# @Email   : ztwu4@iflytek.com
# @File    : mysql_util.py
# @Software: PyCharm

import pymysql
import logging
from DBUtils.PooledDB import PooledDB
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class DB(object):

    __pool = None

    def __init__(self):
        self.pool = DB.__get_conn_pool()

    @staticmethod
    def __get_conn_pool():
        if DB.__pool is None:
            try:
                DB.__pool = PooledDB(
                    creator=pymysql,  # 使用链接数据库的模块
                    maxconnections=2,  # 连接池允许的最大连接数，0和None表示不限制连接数
                    mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
                    maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
                    maxshared=3,  # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
                    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                    maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
                    setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
                    ping=0, # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
                    host='172.31.100.18',
                    port=3306,
                    user='root',
                    password='iflytek',
                    database='tp_manage',
                    charset='utf8'
                )
            except Exception as e:
                logging.error("%s : %s" % (Exception, e))
        print("===pool",DB.__pool.__sizeof__())
        return DB.__pool

    def _get_connection(self):
        conn = self.pool.connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        return conn, cursor

    def _close_connection(self, conn, cursor):
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    def query_sql(self, sql, params=None):
        conn, cursor = self._get_connection()
        print("获取========================================")
        print(conn)
        print(cursor)
        print("获取========================================")
        try:
            cursor.execute(sql, params)
            result = cursor.fetchall()
            self._close_connection(conn, cursor)
        except Exception as e:
            self._close_connection(conn, cursor)
            logging.error(str(e))
            raise Exception("database execute error")
        return result

    def execute_sql(self, sql, params=None):
        conn, cursor = self._get_connection()
        try:
            cursor.execute(sql, params)
            result = cursor.lastrowid
            conn.commit()
            self._close_connection(conn, cursor)
        except Exception as e:
            conn.rollback()
            self._close_connection(conn, cursor)
            logging.error(str(e))
            raise Exception("database commit error")
        return result

    def update_sql(self, sql, params=None):
        conn, cursor = self._get_connection()
        try:
            result = cursor.execute(sql, params)
            conn.commit()
            self._close_connection(conn, cursor)
        except Exception as e:
            conn.rollback()
            self._close_connection(conn, cursor)
            logging.error(str(e))
            raise Exception("database commit error")
        return result