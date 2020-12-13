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
import shutil
import pandas as pd

def split_file(traindatadir, splitnum, splitdir):
    splitfile = {}
    if os.path.exists(splitdir):
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
                    print(line)
                    id = jsonobject["subject"]["id"]
                    name = jsonobject["subject"]["name"]
                    label = jsonobject["subject"]["typeName"]
                    attrname = jsonobject["object"]["typeName"]
                    attrvalue = jsonobject["object"]["name"]
                    type = jsonobject["predication"]["typeName"]
                    if type == "attribute":
                        name = str(name).strip()
                        attrname = str(attrname).strip().replace("：", "")
                        splitno = hash(",".join((label,name)))%splitnum
                        pathfile = splitfile.get(splitno)
                        temp = (id,name,label,attrname,attrvalue)
                        # print(pathfile,splitno,id,name,label,attrname,attrvalue)
                        with open(pathfile,mode="a",encoding="utf-8") as w:
                            w.write("|".join(temp)+"\n")

def train_data(splitdir,datafile,tzfile):
    datas = set()
    print("----in 子进程 pid=%d ,父进程的pid=%d---" % (os.getpid(), os.getppid()))
    path = splitdir + "/" + datafile
    with open(path, mode="r", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if not line:
                break
            linetemp = line.split("|")
            name = linetemp[1]
            label = linetemp[2]
            attrname = linetemp[3]
            datas.add((datafile,name, label, attrname))
    print(datas)
    if len(datas)>0:
        d_analy_tzfb(datas,tzfile)
    msg = "----子进程 pid=%d 完成" % (os.getpid())
    return msg

def d_analy_tzfb(datas,tzfile):
    df = pd.DataFrame(datas)
    df.columns=['文件块', '实体', '类别', '属性']
    type_attr_num = df.groupby(['文件块',"类别","属性"], as_index=False).size().reset_index(name='数量')
    type_num = df[['文件块',"类别","实体"]].drop_duplicates().groupby(['文件块',"类别"], as_index=False).size().reset_index(name='数量')
    # print(type_attr_num.sort_values(["数量"], ascending=False))
    # print(type_num)
    type_attr_df = pd.DataFrame(type_attr_num)
    type_df = pd.DataFrame(type_num)
    data = type_attr_df.merge(type_df, how="inner",left_on="类别",right_on="类别")
    # print(data[data.columns.difference(['文件块_x'])])
    data = data[['文件块_x','类别','属性','数量_x','数量_y']]
    data.to_csv(tzfile,index=False,mode="a",encoding="utf-8",header=False,sep="|")

def analy_tzfb(tzfile,alltzfile):
    print("合并文件===")
    datas = set()
    with open(tzfile, mode="r", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if not line:
                break
            linetemp = line.replace("\n","").split("|")
            fileno = linetemp[0]
            label = linetemp[1]
            attrname = linetemp[2]
            attnum = int(linetemp[3])
            totalnum = int(linetemp[4])
            datas.add((fileno, label, attrname, attnum, totalnum))
    if len(datas)>0:
        data = pd.DataFrame(datas)
        data.columns = ['文件块','类别', '属性', 'attnum', 'totalnum']
        # rs = data.groupby(["类别",'属性'])["attnum","totalnum"].sum()
        # totaldata = data[["类别"]].drop_duplicates()
        totaldata = data[['文件块', "类别", "totalnum"]].drop_duplicates()\
            .groupby(["类别"], as_index=False).sum()
        attnumdata = data[["类别", '属性', 'attnum']].\
            groupby(["类别", '属性'], as_index=False).sum()
        data = totaldata.merge(attnumdata, how="inner", left_on="类别",right_on="类别")
        data['score'] = data.apply(lambda x: x['attnum']/x['totalnum'],axis=1)
        data[['类别','属性','score']].sort_values(["类别","score"], ascending=False)\
            .groupby(['类别']).head(100).to_csv(alltzfile,index=False,mode="w",encoding="utf-8",header=False)
        # print(data[['类别','属性','score']].sort_values(["类别","score"],ascending=False).groupby(['类别']).head(3))

def predict_data(splitdir,datafile,alltzfile,predictfile):
    print("----in 子进程 pid=%d ,父进程的pid=%d---" % (os.getpid(), os.getppid()))
    datas0 = set()
    with open(alltzfile, mode="r", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if not line:
                break
            linetemp = line.split(",")
            name = linetemp[0]
            attrname = linetemp[1]
            score = float(linetemp[2])
            datas0.add((name, attrname,score))
    traindf = pd.DataFrame(datas0)
    traindf.columns = ["类型","属性","得分"]
    traindf = traindf[traindf["得分"] >= 0.1].groupby(["类型"])["属性"].apply(lambda x:list(x))
    # print(traindf)

    datas = set()
    path = splitdir + "/" + datafile
    with open(path, mode="r", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if not line:
                break
            linetemp = line.split("|")
            id = linetemp[0]
            name = linetemp[1]
            type = linetemp[2]
            attrname = linetemp[3]
            datas.add((name, attrname))
    # print(datas)
    if len(datas)>0:
        df = pd.DataFrame(datas)
        df.columns = ["实体","属性"]
        df = df.groupby(["实体"])["属性"].apply(lambda x:list(x))
        df.columns=["实体","属性列表"]
        rsdatas = set()
        # print(df)
        for key,value in df.iteritems():
            print("predict==",key,value)
            for tkey,tvalue in traindf.iteritems():
                print("train==",tkey,tvalue)
                size = len(list(set(value).intersection(set(tvalue))))
                score = size/len(tvalue)
                rsdatas.add((key,tkey,score))
        rsdf = pd.DataFrame(rsdatas)
        rsdf.columns = ["实体","类型","得分"]
        rsdf = rsdf.sort_values(["实体",'得分'],ascending=False).groupby(["实体"]).head(3)
        # print(rsdf)
        rsdf.to_csv(predictfile,index=False,mode="a",encoding="utf-8",header=False,sep="|")
    msg = "----子进程 pid=%d 完成" % (os.getpid())
    return msg

def entity_lable(trainsplitdir, testsplitdir, projectdir):
    if not os.path.exists(projectdir):
        os.makedirs(projectdir)
    temptraindatadir = projectdir+"/temp/traindata"
    temptestdatadir = projectdir+"/temp/testdata"
    tzfile = projectdir+"/tzscore.csv"
    alltzfile = projectdir+"/alltzscore.csv"
    predictfile = projectdir+"/predict.csv"

    results = []
    pool = multiprocessing.Pool(processes=5)

    if os.path.isfile(tzfile):
        os.remove(tzfile)
    if os.path.isfile(predictfile):
        os.remove(predictfile)
    if not os.path.isdir(testsplitdir):
        os.makedirs(testsplitdir)
    if not os.path.isdir(trainsplitdir):
        os.makedirs(trainsplitdir)

    # 文件分片
    split_file(trainsplitdir, 10, temptraindatadir)
    split_file(testsplitdir, 10, temptestdatadir)

    # 并行处理
    files = os.listdir(temptraindatadir)
    for datafile in files:
        result = pool.apply(train_data, (temptraindatadir, datafile, tzfile,))
        results.append(result)

    # 分析提取特征
    analy_tzfb(tzfile, alltzfile)

    # 预测
    files = os.listdir(temptestdatadir)
    for datafile in files:
        result = pool.apply(predict_data, (temptestdatadir, datafile, alltzfile, predictfile,))
        results.append(result)

    pool.close()
    pool.join()
    print(results)

def process_data(datadir, predictfile, projectdir, score):
    df = pd.read_csv(predictfile,sep="|",encoding="utf-8")
    df.columns = ["实体","类型","得分"]
    resultfile = projectdir+"/result.json"
    # resultfile = "result.json"
    # print(df["实体"].tolist())
    df = df[df["得分"]>=score]
    datas = df["实体"].drop_duplicates().tolist()
    print(datas)
    for file in os.listdir(datadir):
        path = datadir + "/" + file
        if os.path.isfile(path):
            print(file)
            with open(path,encoding="utf-8",mode="r") as f1,\
                open(resultfile, encoding="utf-8", mode="w") as f2:
                    while True:
                        line = f1.readline()
                        if not line:
                            break
                        jsonobject = json.loads(line)
                        name = jsonobject["subject"]["name"]
                        if name in datas:
                            f2.write(line)

def start():
    trainsplitdir = "traindata"
    testsplitdir = "testdata"
    temptraindatadir = "temp/traindata"
    temptestdatadir = "temp/testdata"
    tzfile = "tzscore.csv"
    alltzfile = "alltzscore.csv"
    predictfile = "predict.csv"

    results = []
    pool = multiprocessing.Pool(processes=5)

    if os.path.isfile(tzfile):
        os.remove(tzfile)
    if os.path.isfile(predictfile):
        os.remove(predictfile)
    if not os.path.isdir(testsplitdir):
        os.makedirs(testsplitdir)
    if not os.path.isdir(trainsplitdir):
        os.makedirs(trainsplitdir)

    # 文件分片
    split_file(trainsplitdir, 20, temptraindatadir)
    split_file(testsplitdir, 20, temptestdatadir)

    # 并行处理
    files = os.listdir(temptraindatadir)
    for datafile in files:
        result = pool.apply(train_data, (temptraindatadir, datafile, tzfile,))
        results.append(result)

    # 分析提取特征
    analy_tzfb(tzfile,alltzfile)

    # 预测
    files = os.listdir(temptestdatadir)
    for datafile in files:
        result = pool.apply(predict_data, (temptestdatadir, datafile, alltzfile, predictfile,))
        results.append(result)

    pool.close()
    pool.join()
    print(results)

def test():
    datadir = "testdata"
    predictfile = "predict.csv"
    projectdir = ""
    score = 0.4
    process_data(datadir, predictfile, projectdir, score)

if __name__ == '__main__':
    start()
    # test()
