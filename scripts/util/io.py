# coding=utf-8
__author__ = 'liuhu'

import  xdrlib ,sys
import xlrd
import pickle
import os
import numpy as np

from pyExcelerator import *
chrome_row_length=5
data_dir='../data/data.pkl'

def open_excel(file= 'file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e)

def excel_table_byindex(file,colnameindex=0,by_index=0):
    if os.path.exists(data_dir):
        with open(data_dir) as f:
            data_dict=pickle.load(f)
    else:
        data = open_excel(file)
        table = data.sheets()[by_index]
        nrows = table.nrows #行数
        ncols = table.ncols #列数
        colnames =  table.row_values(colnameindex)
        data_dict ={}
        for colname in colnames:
            data_dict[colname]=[]

        data_num=0
        for rownum in range(1,nrows):
            row = table.row_values(rownum)
            if row:
                data_num+=1
                for i in range(len(colnames)):
                    data_dict[colnames[i]].append(row[i])
        data_dict['data_num']=data_num
    return regu_table(data_dict)

def regu_by_name(data_dict,name,regu_li):
    if name!=u'楼层':
        for index,data in enumerate(data_dict[name]):
            data_int=0
            try:
                data_int=int(float(data))
            except:
                data_dict[name][index]=5
                continue
            if data_int<=regu_li[0]:
                data_dict[name][index]=0
            elif data_int<=regu_li[1]:
                data_dict[name][index]=1
            elif data_int<=regu_li[2]:
                data_dict[name][index]=2
            elif data_int<=regu_li[3]:
                data_dict[name][index]=3
            else:
                data_dict[name][index]=4
    else:
        for index,data in enumerate(data_dict[name]):
            if data==regu_li[0]:
                data_dict[name][index]=0
            elif data==regu_li[1]:
                data_dict[name][index]=1
            elif data==regu_li[2]:
                data_dict[name][index]=2
            elif data==regu_li[3]:
                data_dict[name][index]=3
            else:
                data_dict[name][index]=4
    return data_dict

def regu_table(data_dict):
    # keys=[u'均价',u'装修',u'朝向',u'板块',u'挂牌价',u'面积',u'总层数',u'居室数',u'区域',u'楼层',u'小区',u'建筑年代',u'楼型']
    keys=[u'面积',u'总层数',u'居室数',u'楼层',u'建筑年代',u'楼型',u'朝向',u'板块均价']
    # keys=data_dict.keys()# might be part of the keys
    # select cols and regu table

    if not os.path.exists(data_dir):
        with open(data_dir,'wb') as f:
            pickle.dump(data_dict,f)

    data_dict=regu_by_name(data_dict,u'面积',(56,67,88,110))
    data_dict=regu_by_name(data_dict,u'居室数',(1,2,3,4))
    data_dict=regu_by_name(data_dict,u'建筑年代',(1997,2001,2004,2007))
    data_dict=regu_by_name(data_dict,u'总层数',(6,7,15,20))
    data_dict=regu_by_name(data_dict,u'楼层',(u'高楼层',u'低楼层',u'低楼层',u'无数据'))
    data_dict=regu_by_name(data_dict,u'楼型',(u'塔楼',u'板楼',u'板塔结合',u'别墅'))
    data_dict=regu_by_name(data_dict,u'板块均价',(22685,29973,38772,49739))
    #kmeans聚类结果

    name=u'装修'
    for index,data in enumerate(data_dict[name]):
        if data==u'精装':
            data_dict[name][index]=1
        elif data==u'无':
            data_dict[name][index]=2
        else:
            data_dict[name][index]=0

    name=u'朝向'
    for index,data in enumerate(data_dict[name]):
        if data==u'南北':
            data_dict[name][index]=0
        elif data==u'南':
            data_dict[name][index]=1
        elif data==u'西':
            data_dict[name][index]=2
        elif data.find(u'南')==1:
            data_dict[name][index]=3
        elif data==u'无':
            data_dict[name][index]=5
        else:
            data_dict[name][index]=4
    # data_dict['data_num']=1000
    # for key in keys:
    #     data_dict[key]=np.random.random_integers(0,4,data_dict['data_num'])

    return keys,data_dict