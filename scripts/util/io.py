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

def regu_table(data_dict):
    keys=[u'均价',u'装修',u'朝向',u'板块',u'挂牌价',u'面积',u'总层数',u'居室数',u'区域',u'楼层',u'小区',u'编号',u'建筑年代',u'楼型']
    # keys=data_dict.keys()# might be part of the keys
    # select cols and regu table

    if not os.path.exists(data_dir):
        with open(data_dir,'wb') as f:
            pickle.dump(data_dict,f)

    # data_dict['data_num']=1000
    for key in keys:
        data_dict[key]=np.random.random_integers(0,4,data_dict['data_num'])

    return keys,data_dict