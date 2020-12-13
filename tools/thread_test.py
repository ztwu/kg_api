# -*- coding: utf-8 -*-
# @Time    : 2020/9/15 16:14
# @Author  : ztwu4
# @Email   : ztwu4@iflytek.com
# @File    : thread_test.py
# @Software: PyCharm
import multiprocessing
import threading
import time
import os

def test(name):
    thread_name = threading.current_thread().getName()
    pid = os.getpid()
    print('进程【%s】，线程【%s】正在处理任务【%d】：do something...' % (pid, thread_name, name))
    time.sleep(3)
    print('进程【%s】，线程【%s】正在处理任务【%d】：done...' % (pid,thread_name, name))

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=5)
    w_start = time.time()
    for item in range(10):
        pool.apply_async(test, (item,))
    pool.close()
    pool.join()
    print(time.time() - w_start)
    print('任务执行结束')

