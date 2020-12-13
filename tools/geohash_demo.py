# -*- coding: utf-8 -*-
# @Time    : 2020/11/17 16:10
# @Author  : ztwu4
# @Email   : ztwu4@iflytek.com
# @File    : geohash_demo.py
# @Software: PyCharm

import geohash2
print(geohash2.encode(40.222012, 116.248283,8))
print(geohash2.decode("sqbwqpvwsxm4uf8tdy"))