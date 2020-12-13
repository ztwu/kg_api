# -*- coding: utf-8 -*-
# @Time    : 2020/11/19 11:07
# @Author  : ztwu4
# @Email   : ztwu4@iflytek.com
# @File    : encode.py
# @Software: PyCharm
import uuid


def code():
    s = '中文'
    print(s)  # 中文

    str1 = s.encode("gbk")  # 将unicode的编码转化成gbk的编码，获得bytes类型对象
    print(str1, type(str1))  # b'\xd6\xd0\xce\xc4' <class 'bytes'>

    str2 = str1.decode('gbk')  # 将gbk解码成unicode的字符串，获得字符串类型
    print(str2, type(str2))  # 中文 <class 'str'>
    print(isinstance(str2, str))  # True

    str3 = s.encode('utf-8')  # 将unicode编码成utf-8的字符串，获得bytes类型对象
    print(str3, type(str3))  # b'\xe4\xb8\xad\xe6\x96\x87' <class 'bytes'>

    str4 = str3.decode('utf-8')  # 将utf-8解码成unicode的字符串，获得字符串类型
    print(str4, type(str4))  # 中文 <class 'str'>

print(str(uuid.uuid4()).encode('ascii'))

s = "\\u5e74\\u7d93"
print(s.encode('latin-1').decode('unicode_escape'))
code()