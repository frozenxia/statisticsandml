import pandas  as pd
from collections import namedtuple
from pprint import pformat
import numpy as np
from recordtype import recordtype

class Node(recordtype('Node','data clss leaf children split')):
    # def __repr__(self):
    #     return pformat(self)
    pass



def mk_decision_tree(pdsets,gaThreshold=0):
    # print(pdsets)
    # clsSets = set(pdsets['label'])
    # #only one class
    # if(len(clsSets)) == 1:
    #     return Node(data=pdsets,clss=clsSets.pop(),leaf=True,children=None,split=None)
    ga = -1
    gcol = -1
    # decide which index to split 
    for col in pdsets.columns.values:
        if col == 'label' :
            continue
        tga = get_mutual_information(pdsets,col)
        if ga < tga :
            ga = tga
            gcol = col
    # if ga < gaThreshold ,then mark T as leaf
    if ga <= gaThreshold:
        # labelNums = get_set_class_count(pdsets)
        # lc = 0
        # lk = 0
        # for k,v in labelNums.items():
        #     if lc < v:
        #         lc = v
        #         lk = k
        lk = get_node_label(pdsets)
        return Node(data=pdsets,clss=lk,leaf=True,children=None,split=None)
    

    gSets = set(pdsets[gcol])
    children = {}
    for k in gSets:
        children[k] = mk_decision_tree(pdsets[pdsets[gcol]==k])
    return  Node(data=pdsets,clss=None,leaf=False,children=children,split=gcol)

def get_node_label(pdsets):
    labelNums = get_set_class_count(pdsets)
    lc = 0
    lk = None
    for k,v in labelNums.items():
        if lc < v:
            lc = v
            lk = k
    return lk

def get_loss(root,alph=0):
    if (root == None or root.leaf):
        return 0
    cat1 = 0.0
    for k,v in root.children.items():
        # print(k,cat1)
        # print(len(v.data))
        # print(v.data)
        # print(get_set_information(v.data))
        cat1 = cat1 + float(len(v.data)) * get_set_information(v.data)
    # print(cat1)
    cat = cat1 + alph*len(root.children)
    return cat



def reduce_decision_tree(root,alpha):
    if root.leaf == True:
        return True        
    for k,v in root.children.items():
        reduce_decision_tree(v,alpha)
    cat1 = get_loss(root,alpha)
    cat2 = len(root.data)*get_set_information(root.data)

    if(cat1 > cat2):
        # print(root.leaf)
        root.leaf = True
        root.children = None
        root.clss = get_node_label(root.data)
        root.split = None
        return True
    return False

def get_set_class_count(pdsets):
    labelSets = set(pdsets['label'])
    labelNums = {}
    for label in labelSets :
        labelNums[label] = len(pdsets[pdsets['label']==label].index)
    return labelNums

def get_mutual_information(pdsets,col):
    return get_set_information(pdsets) - get_set_condition_information(pdsets,col=col)

def get_mutual_information_ratio(pdsets,col):
    setInfo = get_set_information(pdsets,col=col)
    if setInfo == 0:
        return 0
    return get_mutual_information(pdsets,col)/get_set_information(pdsets,col=col)


def get_set_condition_information(pdsets,col):
    clsNums = {}
    for index ,row in  pdsets.iterrows():
        clsNums[row[col]] = clsNums.get(row[col],0) + 1
    # print clsNsuminplums
    totalCount = len(pdsets.index)
    sum = 0.0
    for k ,v in clsNums.items():
        subsetInfo = get_set_information(pdsets[pdsets[col]==k])
        sum += (float(v)/totalCount)*subsetInfo
    return sum

def get_set_information(pdsets,col = 'label'):
    # print('\n',pdsets,'\n')
    # print ('col=',col)
    labelSets = set(pdsets[col])
    labelNums = {}
    for label in labelSets :
        labelNums[label] = len(pdsets[pdsets[col]==label].index)
    totalCount = len(pdsets.index)
    sum = 0.0
    for k,v in labelNums.items():
        sum += -(float(v)/totalCount)*np.log2(float(v)/totalCount)
    return sum


def get_entropy():
        # print (index ,row)
    pass


if __name__ =='__main__':
    datas = [[1,3,'abc',-1],[2,3,'abc',1],[2,3,'asbc',-1]]
    pdsets = pd.DataFrame(datas)
    pdsets.rename(columns={3:'label'},inplace=True)  # clsSets = set(pdsets['label'])
    # #only one class
    # if(len(clsSets)) == 1:
    #     return Node(data=pdsets,clss=clsSets.pop(),leaf=True,children=None,split=None)ace=True)
    # print(get_set_information(pdsets,col=1))
    # print(get_set_information(pdsets,col=0))
    # print(get_mutual_information_ratio(pdsets,0))
    # print(get_mutual_information_ratio(pdsets,1))
    # print(get_mutual_information_ratio(pdsets,2))
    # print(get_mutual_information_ratio(pdsets,0))
    # print(get_mutual_information_ratio(pdsets,2))
    # print(get_mutual_information(pdsets,2))   # get the split index 
    # print(mk_decision_tree(pdsets))
    tr = mk_decision_tree(pdsets)

    cat = get_loss(tr)
    print(cat)

    reduce_decision_tree(tr,0)
    print(tr)