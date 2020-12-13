# -*- coding: utf-8 -*-
# @Time    : 2020/12/2 9:58
# @Author  : ztwu4
# @Email   : ztwu4@iflytek.com
# @File    : thread_test3.py
# @Software: PyCharm

import asyncio
import time


async def test(a,b):
    for i in range(10000000):
        a += 1
        b += 1
    print(a, b)
    return a,b

async def hello1(a, b):
    print('准备做加法运算')
    future = await test(a,b)
    print(future)
    return a + b

loop = asyncio.get_event_loop()
t1 = time.time()  # 开始时间
print(t1)
tasks = []
for i in range(1,10):
    print(i)
    tasks.append(hello1(i, i+1))
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
t2 = time.time()# 结束时间
print(t2)
print(t2 - t1)  # 时间间隔