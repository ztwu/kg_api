# -*- coding: utf-8 -*-
# @Time    : 2020/3/10 17:57
# @Author  : ztwu4
# @Email   : ztwu4@iflytek.com
# @File    : entity_class_util.py
# @Software: PyCharm

# 获取特征数据
import json
import multiprocessing
import os
import re
import shutil
import pandas as pd

def split_file(traindatadir, splitnum, splitdir, configpath):
    splitfile = {}
    if os.path.isdir(splitdir):
        shutil.rmtree(splitdir)
    os.makedirs(splitdir)
    for num in range(splitnum):
        path = splitdir+"/data"+str(num)+".json"
        if not os.path.isfile(path):
            fd = open(path, mode="w", encoding="utf-8")
            fd.close()
        splitfile.setdefault(num,path)
    # print(splitfile)

    list = os.listdir(traindatadir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(traindatadir, list[i])
        if os.path.isfile(path):
            with open(path, mode="r", encoding="utf-8") as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    jsonobject = json.loads(line)
                    id = jsonobject["subject"]["id"]
                    name = jsonobject["subject"]["name"]
                    label = jsonobject["subject"]["typeName"]
                    attrname = jsonobject["object"]["typeName"]
                    attrvalue = jsonobject["object"]["name"]
                    type = jsonobject["predication"]["typeName"]
                    if type == "attribute":
                        name = str(name).strip()
                        attrname = str(attrname).strip().replace("：", "")
                        splitno = hash(label)%splitnum
                        pathfile = splitfile.get(splitno)
                        temp = (id,name,label,attrname,attrvalue)
                        # print(pathfile,splitno,id,name,label,attrname,attrvalue)
                        with open(pathfile,mode="a",encoding="utf-8") as w:
                            w.write("|".join(temp)+"\n")

def train_data(splitdir,datafile,tempfile):
    # traindf = pd.read_csv("../kg_entity_label/alltzscore.csv",encoding="utf-8")
    # traindf.columns = ["类型", "属性", "得分"]
    # print(traindf[traindf['得分']>=0.5])
    datas = set()
    print("----in 子进程 pid=%d ,父进程的pid=%d---" % (os.getpid(), os.getppid()))
    path = splitdir + "/" + datafile
    with open(path, mode="r", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if not line:
                break
            linetemp = line.replace("\n","").split("|")
            name = linetemp[1]
            label = linetemp[2]
            attrname = linetemp[3]
            attrvalue = linetemp[4]
            if len(re.findall("[\d]+[年]|[\d]+[月]|[\d]+[日]", attrvalue))>0:
                datas.add((name, label, 0, attrvalue))
            else:
                datas.add((name, label, 1, attrvalue))
    print(datas)
    if len(datas)>0:
        d_analy_tzfb(datas,tempfile)
    msg = "----子进程 pid=%d 完成" % (os.getpid())
    return msg

def d_analy_tzfb(datas,tempfile):
    df = pd.DataFrame(datas)
    df.columns=['实体', '类别', 'type', '属性']
    df0 = df[df["type"]==0]
    df1 = df[df["type"]==1]
    df0 = df0[['实体', '类别', '属性']]
    df1 = df1[['实体', '类别', '属性']]
    rs0 = df0.groupby(['实体', '类别'])["属性"].apply(lambda x:list(x))
    rs1 = df1.groupby(['实体', '类别'])["属性"].apply(lambda x:list(x))
    rsdatas = list()
    for index,row in rs0.iteritems():
        for tindex, trow in rs0.iteritems():
            if tindex[0] != index[0] and tindex[1] == index[1]:
                size = len(list(set(trow).intersection(set(row))))
                allsize = len(list(set(trow).union(set(row))))
                score = size / allsize
                rsdatas.append((index[0],tindex[0],score*0.2))
    for index,row in rs1.iteritems():
        for tindex, trow in rs1.iteritems():
            if tindex[0] != index[0] and tindex[1] == index[1]:
                size = len(list(set(trow).intersection(set(row))))
                allsize = len(list(set(trow).union(set(row))))
                score = size / allsize
                rsdatas.append((index[0],tindex[0],score*0.8))

    if len(rsdatas) > 0:
        rsdf = pd.DataFrame(rsdatas)
        rsdf.columns = ["实体1", "实体2", "score"]
        rsdf = rsdf[rsdf["score"] >= 0.01].groupby(["实体1", "实体2"], as_index=False).sum()
        # print(rsdf)
        rsdf[rsdf["score"] >= 0.01].sort_values(["实体1", "score"], ascending=False).groupby(["实体1"]).head(3) \
            .to_csv(tempfile, encoding="utf-8", index=False, mode="a", header=False)

def process_data(tempfile,predictfile):
    rsdf = pd.read_csv(tempfile,encoding="utf-8")
    rsdf.columns = ["实体1", "实体2", "score"]
    rsdf = rsdf.drop_duplicates()
    rsdf = rsdf[rsdf["score"] >= 0.01]
    rsdf.sort_values(["实体1", "score"], ascending=False).groupby(["实体1"]).head(3) \
        .to_csv(predictfile, encoding="utf-8", index=False, mode="w", header=False)

def start():
    configpath = "../../../jswqzb/武器装备本体.yaml"
    temptraindatadir = "temp/traindata"
    trainsplitdir = "traindata"
    predictfile = "predict.csv"
    tempfile = "temppredict.csv"

    results = []
    pool = multiprocessing.Pool(processes=5)

    if os.path.isfile(tempfile):
        os.remove(tempfile)
    if not os.path.isdir(trainsplitdir):
        os.makedirs(trainsplitdir)

    # 文件分片
    split_file(trainsplitdir, 5, temptraindatadir, configpath)

    # # 并行处理
    files = os.listdir(temptraindatadir)
    for datafile in files:
        result = pool.apply(train_data, (temptraindatadir, datafile, tempfile))
        results.append(result)

    process_data(tempfile,predictfile)

    pool.close()
    pool.join()
    print(results)

def test():
    # predictfile = "predict.csv"
    # tempfile = "temppredict.csv"
    # process_data(tempfile, predictfile)
    # value = "10月"
    value = "2019-10"
    print(re.findall("[\d]+[年]|[\d]+[月]|[\d]+[日]",value))

if __name__ == '__main__':
    start()
    # test()
