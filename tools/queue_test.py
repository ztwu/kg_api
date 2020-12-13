# -*- coding: utf-8 -*-
# @Time    : 2020/9/15 16:36
# @Author  : ztwu4
# @Email   : ztwu4@iflytek.com
# @File    : queue_test.py
# @Software: PyCharm

import time
import random
from multiprocessing import JoinableQueue, Process


def consumer(jq, name):
    while True:
        food = jq.get()
        time.sleep(random.uniform(1, 2))
        print('%s吃完%s' % (name, food))
        jq.task_done()


def producer(jq):
    for i in range(1, 10):
        time.sleep(random.random())
        food = '甜品%s' % i
        print('%s生产了%s' % ('满记甜品店', food))
        jq.put(food)
    jq.join()


if __name__ == '__main__':
    jq = JoinableQueue(5)
    c1 = Process(target=consumer, args=(jq, 'doony'))
    p1 = Process(target=producer, args=(jq,))
    c1.daemon = True
    c1.start()
    p1.start()
    p1.join()