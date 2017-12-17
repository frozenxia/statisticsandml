from numpy import *

def loadSample():
    dataIn = matrix([[1],[2],[3],[4],[5],[6],[7],[8],[9],[10]])
    yValues = [5.56,5.70,5.91,6.40,6.80,7.05,8.90,8.70,9.00,9.05]
    return dataIn,yValues

def getC(dataMatrix,threshVal,dim,yMatrix,inequal):
    if inequal == 'lt':
        yc1 = yMatrix[dataMatrix[:,dim] <=  threshVal].T
        # print(yc1)
        m,n = shape(yc1)
        if m == 0:
            c1 = 0
            m1 = 0
            yn1 = [[]]
        else :
            c1 = yc1.sum()/m
            m1 = float((yc1.T -c1)*(yc1-c1))
            yn1 = array(yc1-c1)
    else :
        
        yc1 = yMatrix[dataMatrix[:,dim] >  threshVal].T
        # print('yMatrix',yMatrix)
        # print('yc1',yc1)
        m,n = shape(yc1)
        if m == 0:
            c1 = 0
            m1 = 0
            yn1 = [[]]
        else :
            c1 = yc1.sum()/shape(yc1)[0]
            m1 = float((yc1.T -c1)*(yc1-c1))
            yn1 = array(yc1-c1)
    return c1,m1,yn1

def getResiduelSplit(dataIn,yValues):
    dataMatrix = mat(dataIn)
    yMatrix = mat(yValues).T
    # print(yMatrix)
    m,n = shape(dataMatrix)
    numSteps = 10
    dim = 0
    minM = Inf
    split = 0
    yNew = None
    for i in range(n):
        rangeMin = dataMatrix[:,i].min()
        rangeMax = dataMatrix[:,i].max()
        # print(rangeMin,rangeMax)
        step = (rangeMax-rangeMin)/numSteps
        for j in range(-1,numSteps+1):
            threshVal =  rangeMin + float(j) * step
            # print('threshVal',threshVal)
            c1,m1,yn1= getC(dataMatrix,threshVal,i,yMatrix,'lt')
            c2,m2,yn2= getC(dataMatrix,threshVal,i,yMatrix,'gt')

            if (m1+m2 < minM):
                dim = i
                minM = m1+m2
                split = threshVal
                yNew = append(yn1,yn2)
                # yNew.append(yn1)
                # yNew.append(yn2)
            # print(c1,m1)
            # print(c2,m2)

            # break
        # break
    return dim,split,minM,yNew


def tree_boosting(dataIn,yValues,iterVal,thresh):
    args = []
    yv = yValues
    for i in range(iterVal):
        mp = {}
        dim,split,minM,yn = getResiduelSplit(dataIn,yv)
        # if (minM)
        mp['dim'] = dim
        mp['split'] = split
        args.append(mp)
        print(dim,split,minM,yn)
        if minM <= thresh:
            break
        yv = yn

    return args 


dataIn,yValues = loadSample()
# dim,split,yn = getResiduelSplit(dataIn,yValues)
# print(dim,split,yn)
args = tree_boosting(dataIn,yValues,10,0.17)

print(args)