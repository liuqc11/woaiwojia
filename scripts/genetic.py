# coding=utf-8
__author__ = 'liuhu'

import random
import sys
import numpy as np
from util import io

keys, collection=io.excel_table_byindex('../data/23000.xlsx')
chrome_col_length=len(keys)
chrome_chosen_col_length=3
chrome_row_length=5

def crossover(pop, pc):
    #crossover every two chromes by chance of pc
    popsize, chromelength=pop.shape
    newpop=pop

    for i in range(0,popsize,2):
        ra=np.random.rand()
        if ra<pc:
            se_col=np.random.permutation(range(chrome_col_length))[:2]
            se_rows=np.random.permutation(range(chrome_col_length,chromelength))[:2]
            se_col=np.sort(se_col)
            se_rows=np.sort(se_rows)

            newpop[i,se_col[0]:se_col[1]]=pop[i+1,se_col[0]:se_col[1]]
            newpop[i+1,se_col[0]:se_col[1]]=pop[i,se_col[0]:se_col[1]]

            newpop[i,se_rows[0]:se_rows[1]]=pop[i+1,se_rows[0]:se_rows[1]]
            newpop[i+1,se_rows[0]:se_rows[1]]=pop[i,se_rows[0]:se_rows[1]]

        #ensure num of chosen_col be constant
        for j in [i,i+1]:
            num=sum(newpop[j,:chrome_col_length])
            if num > chrome_chosen_col_length:
                ones=[index for index,npop in enumerate(newpop[j,:chrome_col_length]) if npop==1]
                tozeros=np.random.permutation(ones)[:num-chrome_chosen_col_length]
                newpop[j,tozeros]=0
            elif num < chrome_chosen_col_length:
                zeros=[index for index,npop in enumerate(newpop[j,:chrome_col_length]) if npop==0]
                toones=np.random.permutation(zeros)[:chrome_chosen_col_length-num]
                newpop[j,toones]=1
    return newpop

def mutation(pop, pm, p_col=0.5):
    #mutation every chrome by chance of pm and p_col
    popsize, chromelength=pop.shape
    newpop=pop
    for i in range(popsize):
        if np.random.rand()>pm:
            continue

        if np.random.rand()<p_col:
            ones=[index for index,npop in enumerate(newpop[i,:chrome_col_length]) if npop==1]
            zeros=[index for index,npop in enumerate(newpop[i,:chrome_col_length]) if npop==0]
            index1=np.random.permutation(ones)[0]
            index0=np.random.permutation(zeros)[0]
            newpop[i,index1]=0
            newpop[i,index0]=1
        else:
            index=int(chrome_col_length+np.floor(np.random.rand()*(chromelength-chrome_col_length)))
            newpop[i,index]=1-newpop[i,index]

    return newpop

def selection(pop, fvalue):
    #selection by fvalue and randperm
    fvalue=fvalue/sum(fvalue)
    fvalue=fvalue.cumsum()

    popsize=pop.shape[0]
    newpop=np.zeros(pop.shape)
    newindexs=[]
    for i in range(popsize):
        ra=np.random.rand()
        chosen_index=0
        for index,f in enumerate(fvalue):
            if f>ra:
                chosen_index=index-1
                break
        newindexs.append(chosen_index)

    newindexs=np.random.permutation(newindexs)
    for i,newindex in enumerate(newindexs):
        newpop[i,:]=pop[newindex,:]
    return newpop

def objective(pop, keys, collection):
    subsets=get_subsets_by_pops(pop, keys, collection)
    objvalues=[]
    min_length=200

    max_objvalue=-1
    best_data={}
    for subset in subsets:
        if len(subset['jjzq'])<min_length or len(subset['jzzq'])<min_length:
            objvalue=0
        else:
            meanjjzq=np.mean(subset['jjzq'])
            meanjjj=np.mean(subset['jjj'])
            meanjzzq=np.mean(subset['jzzq'])
            meanjzj=np.mean(subset['jzj'])

            stdjjzq=np.std(subset['jjzq'])
            stdjjj=np.std(subset['jjj'])
            stdjzzq=np.std(subset['jzzq'])
            stdjzj=np.std(subset['jzj'])

            objvalue=abs(meanjjzq-meanjzzq)/(stdjjzq+stdjzzq)+abs(meanjjj-meanjzj)/(stdjjj+stdjzj)
            if objvalue>max_objvalue:
                max_objvalue=objvalue
                best_data['简装房数目']=len(subset['jjj'])
                best_data['精装房数目']=len(subset['jzj'])
                best_data['简装周期均值']=meanjjzq
                best_data['精装周期均值']=meanjzzq
                best_data['简装周期方差']=stdjjzq
                best_data['精装周期方差']=stdjzzq

                best_data['简装价均值']=meanjjj
                best_data['精装价均值']=meanjzj
                best_data['简装价方差']=stdjjj
                best_data['精装价方差']=stdjzj
        objvalues.append(objvalue)

    return np.array(objvalues),best_data

def fitvalue(objvalue):
    fvalue=objvalue
    return fvalue

def genetic():
    #input:
    ## popsize: population size
    ## pc: crossover prob
    ## pm: mutation prob
    ## maxIter: maxIterations

    #output:
    ##x: bestfit (maxIter*1)
    ##y: bestindividual (maxIter*chromlength)
    if len(sys.argv)==1:
        popsize = 200
        pc = 0.6
        pm = 0.6
        maxIter = 100
    elif len(sys.argv)==5:
        popsize = int(sys.argv[1])
        pc = float(sys.argv[2])
        pm = float(sys.argv[3])
        maxIter = int(sys.argv[4])
    else:
        print 'python genetic.py popsize crossover_prob mutation_prob max_iteration'
        return 0,0

    chromlength=len(keys)+chrome_chosen_col_length*chrome_row_length
    pop = np.round(np.random.rand(popsize, chromlength))

    x = np.zeros((maxIter, 1))
    y = np.zeros((maxIter, chromlength))

    bestfit=-1
    bestindividual=[]

    for iter in range(maxIter):
        objvalue,best_data = objective(pop, keys, collection) # popsize * chromlength vector
        fvalue=fitvalue(objvalue) # calculate fit values
        #if not better than prev generation
        if bestfit>np.amax(fvalue):
            negest=np.argmin(fvalue)
            pop[negest,:]=bestindividual
        else:
            bestfit=np.amax(fvalue)
            index=np.argmax(fvalue)
            bestindividual = pop[index, :]
            #print n iteration before
#            print iter,bestfit
#            for m_in in range(len(keys)):
#                if bestindividual[m_in]==1:
#                    print keys[m_in]
            print bestfit
            print iter,bestindividual
            best_data_keys=['简装房数目','精装房数目','简装价均值','精装价均值','简装价方差','精装价方差','简装周期均值','精装周期均值','简装周期方差','精装周期方差']
            for key in best_data_keys:
                print key,best_data[key]
            sys.stdout.flush()
            
        
        newpop = selection(pop, fvalue) # selection procedure
        newpop = crossover(newpop, pc) # cross-over procedure
        newpop = mutation(newpop, pm) # mutation procedure

        x[iter] = bestfit
        y[iter] = bestindividual

        pop=newpop

    return x,y

#100101 101 001 010
def get_subsets_by_pops(pop, keys, collection):
    popsize=pop.shape[0]
    # chrome_col_length=len(keys)#???
    # chrome_chosen_col_length=sum(pop[0,:chrome_col_length])
    # chrome_row_length=(pop.shape[1]-chrome_col_length)/chrome_chosen_col_length
    subset=[{'jzzq':[],'jzj':[],'jjzq':[],'jjj':[]} for i in range(popsize)]
    data_num=collection['data_num']
    for pop_index in range(popsize):
        pop_cols=pop[pop_index,:chrome_col_length]
        pop_keys=[keys[index] for index,k in enumerate(pop_cols) if k==1]

        pop_values=pop[pop_index,chrome_col_length:]
        # pop_rows=[ for index in range(0,chrome_chosen_col_length*chrome_row_length,chrome_row_length)]

        for index in range(data_num):
            ok=True
            for key_index,key in enumerate(pop_keys):
                if key_index>=chrome_chosen_col_length:
                    break
                field=collection[key][index]
                if field == 5 or pop_values[key_index*chrome_row_length+field]==0:
                    ok=False
                    break
            if ok:
                if collection[u'装修'][index]==0:
                    # 简装
                    subset[pop_index]['jjzq'].append(collection[u'成交周期'][index])
                    subset[pop_index]['jjj'].append(collection[u'成交价'][index])
                elif collection[u'装修'][index]==1:
                    # 精装
                    subset[pop_index]['jzzq'].append(collection[u'成交周期'][index])
                    subset[pop_index]['jzj'].append(collection[u'成交价'][index])
    return subset

if __name__=="__main__":
    bestfit,bestindividual=genetic()
