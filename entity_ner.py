# -*- coding: utf-8 -*-
# @Time    : 2020/4/24 10:16
# @Author  : ztwu4
# @Email   : ztwu4@iflytek.com
# @File    : entity_ner.py
# @Software: 命名实体识别
from tools.ltp_util import LtpParser

def entity_ner(content):
    result = {}
    entitielist = list()
    if len(content) > 0:
        parse = LtpParser()
        entities = parse.comm_ner(content)
        parse.release_model()
        print(entities)
        for item in entities:
            temp = {}
            temp.setdefault("type",item[1])
            temp.setdefault("entity_name",item[0])
            entitielist.append(temp)
    result.setdefault("code",200)
    result.setdefault("entities",entitielist)
    return result