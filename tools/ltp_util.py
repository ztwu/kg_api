# -*- coding: utf-8 -*-
# @Time    : 2020/3/10 17:57
# @Author  : ztwu4
# @Email   : ztwu4@iflytek.com
# @File    : ltp_util.py
# @Software: ltp
import os
import jieba
import pandas as pd
import numpy as np
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller

class LtpParser:

    def __init__(self):
        LTP_DIR = "/home/python/ltp/ltp_data_v3.4.0"

        # 分词模型，单文件
        self.segmentor = Segmentor()
        self.segmentor.load(os.path.join(LTP_DIR, "cws.model"))

        # 词性标注模型，单文件
        self.postagger = Postagger()
        self.postagger.load(os.path.join(LTP_DIR, "pos.model"))

        # 依存句法分析模型，单文件
        self.parser = Parser()
        self.parser.load(os.path.join(LTP_DIR, "parser.model"))

        # 命名实体识别模型，单文件
        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(os.path.join(LTP_DIR, "ner.model"))

        # 语义角色标注模型，多文件
        self.labeller = SementicRoleLabeller()
        self.labeller.load(os.path.join(LTP_DIR, 'pisrl.model'))

    def release_model(self):
        # 释放模型
        self.segmentor.release()
        self.postagger.release()
        self.recognizer.release()
        self.parser.release()
        self.labeller.release()

    # 命名实体识别
    def entity_ner(self, words, postags):
        netags = self.recognizer.recognize(words, postags)  # 命名实体识别
        entity_ner = list()
        for word, ntag in zip(words, netags):
            entity_ner.append((word,ntag))
        return entity_ner

    # 语义角色标注
    def format_labelrole(self, words, postags):
        arcs = self.parser.parse(words, postags)
        roles = self.labeller.label(words, postags, arcs)
        roles_dict = {}
        for role in roles:
            roles_dict[role.index] = {arg.name: [arg.name, arg.range.start, arg.range.end] for arg in role.arguments}
        return roles_dict

    # 句法分析---为句子中的每个词语维护一个保存句法依存儿子节点的字典
    def build_parse_child_dict(self, words, postags, arcs):
        child_dict_list = []
        format_parse_list = []
        for index in range(len(words)):
            child_dict = dict()
            for arc_index in range(len(arcs)):
                if arcs[arc_index].head == index + 1:  # arcs的索引从1开始
                    if arcs[arc_index].relation in child_dict:
                        child_dict[arcs[arc_index].relation].append(arc_index)
                    else:
                        child_dict[arcs[arc_index].relation] = []
                        child_dict[arcs[arc_index].relation].append(arc_index)
            child_dict_list.append(child_dict)
        rely_id = [arc.head for arc in arcs]  # 提取依存父节点id
        relation = [arc.relation for arc in arcs]  # 提取依存关系
        heads = ['Root' if id == 0 else words[id - 1] for id in rely_id]  # 匹配依存父节点词语
        for i in range(len(words)):
            # ['ATT', '李克强', 0, 'nh', '总理', 1, 'n']
            a = [relation[i], words[i], i, postags[i], heads[i], rely_id[i] - 1, postags[rely_id[i] - 1]]
            format_parse_list.append(a)
        return child_dict_list, format_parse_list

    # 通用实体识别
    def comm_ner(self, sentence):
        class_entity = {
            "Ni": "institution",
            "Ns": "place",
            "Nh": "name"
        }
        words = jieba.cut(sentence)
        words = [word for word in words]
        postags = list(self.postagger.postag(words))
        entity_ner = self.entity_ner(words,postags)
        result = set()
        entity = list()
        index = 0
        for item in entity_ner:
            entity_name = item[0]
            entity_bz = item[1]
            temp = entity_bz.split("-")
            if len(temp) == 2:
                bz = temp[0]
                type = temp[1]
                if bz == "S":
                    result.add((entity_name,class_entity.get(type)))
                else:
                    entity.append((index,entity_name,class_entity.get(type)))
                    if bz == "E":
                        index = index+1
        if len(entity) > 0:
            entitydf = pd.DataFrame(entity)
            resulttemp = entitydf.groupby([0,2])[1].apply(lambda x : "".join(list(x))).reset_index(name='实体名称')
            for item in np.array(resulttemp[["实体名称",2]]).tolist():
                result.add(tuple(item))
        print("ltp=",result)
        return result