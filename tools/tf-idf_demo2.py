# -*- coding: utf-8 -*-
# @Time    : 2020/11/17 14:43
# @Author  : ztwu4
# @Email   : ztwu4@iflytek.com
# @File    : tf-idf_demo2.py
# @Software: PyCharm

# 读取文档
# 对要计算的多篇文档进行分词
# 对文档进行整理成指定格式，方便后续进行计算
# 计算出词语的词频
# 【可选】对词频低的词语进行过滤
# 建立语料库词典
# 加载要对比的文档
# 将要对比的文档通过doc2bow转化为词袋模型
# 对词袋模型进行进一步处理，得到新语料库
# 将新语料库通过tfidfmodel进行处理，得到tfidf
# 通过token2id得到特征数
# 稀疏矩阵相似度，从而建立索引
# 得到最终相似度结果

import jieba as jb
from gensim import corpora,models,similarities
##地址库
place0="江苏省南京市玄武区徐庄软件园苏宁大道一号苏宁易购总部"
place1="江苏省镇江市宝华镇苏宁智慧小镇智慧村12号"
place2="安徽省合肥市肥东区无名街道某小区56栋402"
place3="安徽省合肥市肥东区有名街道某小区12栋502"
place4="山东省威海市环翠区新威路13号苏宁快递点"
place5="山东省烟台市环翠区新威路18号天天快递点"
place6="玄武区仙居雅苑23栋102"
place7="江苏省南京市玄武区仙鹤门街道仙居雅苑17栋304"

# test_place="江苏省南京市玄武区仙鹤门街道仙居雅苑23栋102"
test_place="江苏省南京市玄武区"
#test_place="上海金钊机电设备有限公司"
##将地址库存到列表中
all_place=[]
all_place.append(place0)
all_place.append(place1)
all_place.append(place2)
all_place.append(place3)
all_place.append(place4)
all_place.append(place5)
all_place.append(place6)
all_place.append(place7)

##对列表中的地址进行分词
all_place_list=[]
for place in all_place:
    place_list=[word for word in jb.cut(place)]
    all_place_list.append(place_list)

##将测试地址进行分词并保存在test_place_list
test_place_list=[word for word in jb.cut(test_place)]
##利用地址库生成字典
dictionary=corpora.Dictionary(all_place_list)
#dictionary.keys() 查看字典中的编号
# for key, value in dictionary.token2id.items(): #查看编号与词的对应关系
#     print(key,value)
##利用doc2bow制作语料库（实际上就是稀疏矩阵【编号：词频】）
corpus=[dictionary.doc2bow(doc) for doc in all_place_list]
print(corpus)
##corpus
##将测试地址也转变成稀疏矩阵形式
test_place_vec=dictionary.doc2bow(test_place_list)
print(test_place_vec)
#test_place_vec

###相似度分析
###使用TF—IDF对语料库进行建模
tfidf=models.TfidfModel(corpus)
##获取测试地址每个词的TF—IDF值
# tfidf[test_place_vec]
##测试文本相似度
index=similarities.SparseMatrixSimilarity(tfidf[corpus],num_features=len(dictionary.keys()))
sim=index[tfidf[test_place_vec]]

sim = sorted(enumerate(sim),key=lambda x:x[1], reverse=True)
for index,score in sim:
    print(all_place[index],score)