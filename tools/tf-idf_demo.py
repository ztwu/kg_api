# -*- coding: utf-8 -*-
# @Time    : 2020/11/17 14:31
# @Author  : ztwu4
# @Email   : ztwu4@iflytek.com
# @File    : tf-idf_demo.py
# @Software: PyCharm

import jieba.posseg as psg
import math
import functools
import numpy as np


# 利用tf-idf算法提权文章关键词


# 加载并返回停用词列表 list
def get_stopword_list():
    stop_word_path = 'stopwords.txt'
    stopword_list = [word.replace('\n', '') for word in open(stop_word_path, encoding='utf-8').readlines()]
    return stopword_list


# 对文本切分，并同词性一并返回为
def split_text_to_list(text):
    word_list = psg.cut(text)
    return word_list


# 去除干扰词：过滤除名词外的其他词性，再判断词是否在停用词表中，长度是否大于等于2等。
def clean_word_list(word_list):
    stopword_list = get_stopword_list()
    cleaned_word_list = []
    # 过滤除名词外的其他词性。不进行词性过滤，则将词性都标记为n,表示全部保留
    for seg in word_list:
        word = seg.word
        flag = seg.flag
        if flag.startswith('n'):
            # 过滤高停用词表中的词，以及长度为<2的词
            if word not in stopword_list and len(word) > 1:
                cleaned_word_list.append(word)
    return cleaned_word_list


# topK
def cmp(e1, e2):
    res = np.sign(e1[1] - e2[1])
    if res != 0:
        return res
    else:
        a = e1[0] + e2[0]
        b = e2[0] + e1[0]
        if a > b:
            return 1
        elif a == b:
            return 0
        else:
            return -1


# 开始提取关键词
def tfidf_extract(cleaned_word_list, keyword_num=10):
    # 加载数据集，并清洗 添加在文档列表中
    # 文档集是一个形如[['a','b', ...], ['c','d', ...], [], ...]的列表
    doc_list = []
    for line in open('text2.txt', 'r', encoding='utf-8'):  # 这里的text2.txt应该是doc_path,我这里只用了一篇文章作为文档集
        word_list = split_text_to_list(line.strip())
        doc_cleaned_word_list = clean_word_list(word_list)
        doc_list.append(doc_cleaned_word_list)
    # 计算idf值
    idf_dic = {}
    doc_count = len(doc_list)  # 文档数
    # 每个词出现的文档数,即一个文章中的词在整个文档中出现的次数
    for doc in doc_list:
        for word in set(doc):
            # 如果idf_dic有word这个key的词，name返回他的value,否则返回默认值0.0
            # {'c1': 2.0, 'b2': 2.0, 'a2': 1.0, 'c2': 1.0, 'b1': 1.0, 'a1': 1.0,......}
            idf_dic[word] = idf_dic.get(word, 0.0) + 1.0  # http://www.runoob.com/python/att-dictionary-get.html
    # 按公式转换为idf值
    for k, v in idf_dic.items():  # 循环字典里面的每一个对象key:value
        idf_dic[k] = math.log(doc_count / (1.0 + v))
    # 对于没有在字典中的词，默认其尽在一个文档出现，得到默认idf值
    default_idf = math.log(doc_count / 1.0)
    # 统计TF值
    tf_dic = {}
    for word in cleaned_word_list:  # 这里的cleaned_word_list表示处理后的待提取文本
        tf_dic[word] = tf_dic.get(word, 0.0) + 1.0
    word_count = len(cleaned_word_list)
    for k, v in tf_dic.items():
        tf_dic[k] = float(v) / word_count
    # 开始计算tf-idf
    tfidf_dic = {}
    for word in cleaned_word_list:
        idf = idf_dic.get(word, default_idf)
        tf = tf_dic.get(word, 0)
        tfidf = tf * idf
        tfidf_dic[word] = tfidf
    # 根据tf-idf排序，取排名前keyword_num的词作为关键词
    for k, v in sorted(tfidf_dic.items(), key=functools.cmp_to_key(cmp), reverse=True)[:keyword_num]:
        print(k + "/", end='')


if __name__ == '__main__':
    text = '6月19日,《2012年度“中国爱心城市”公益活动新闻发布会》在京举行。' + \
           '中华社会救助基金会理事长许嘉璐到会讲话。基金会高级顾问朱发忠,全国老龄' + \
           '办副主任朱勇,民政部社会救助司助理巡视员周萍,中华社会救助基金会副理事长耿志远,' + \
           '重庆市民政局巡视员谭明政。晋江市人大常委会主任陈健倩,以及10余个省、市、自治区民政局' + \
           '领导及四十多家媒体参加了发布会。中华社会救助基金会秘书长时正新介绍本年度“中国爱心城' + \
           '市”公益活动将以“爱心城市宣传、孤老关爱救助项目及第二届中国爱心城市大会”为主要内容,重庆市' + \
           '、呼和浩特市、长沙市、太原市、蚌埠市、南昌市、汕头市、沧州市、晋江市及遵化市将会积极参加' + \
           '这一公益活动。中国雅虎副总编张银生和凤凰网城市频道总监赵耀分别以各自媒体优势介绍了活动' + \
           '的宣传方案。会上,中华社会救助基金会与“第二届中国爱心城市大会”承办方晋江市签约,许嘉璐理' + \
           '事长接受晋江市参与“百万孤老关爱行动”向国家重点扶贫地区捐赠的价值400万元的款物。晋江市人大' + \
           '常委会主任陈健倩介绍了大会的筹备情况。'
    word_list = split_text_to_list(text)
    cleaned_word_list = clean_word_list(word_list)
    print(cleaned_word_list)
    # tfidf_extract(cleaned_word_list)
