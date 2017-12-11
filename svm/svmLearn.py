import numpy as np
import matplotlib.pyplot as plt
import random
from numpy import *
def loadData(fileName):
    dataMat=[]
    labelMat=[]
    with open(fileName) as fp:
        for line in fp.readlines():
            lineArr = line.split('\t')
            dataMat.append([float(lineArr[0]),float(lineArr[1])])
            labelMat.append(float(lineArr[2]))
    return dataMat,labelMat


def plotBestFit(dataIn, labelIn):
    n = shape(dataIn)[0]
    xcord1 = []
    ycord1 = []
    xcord2 = []
    ycord2 = []
    for i in range(n):
        if int(labelIn[i]) == 1:
            xcord1.append(dataIn[i][0])
            ycord1.append(dataIn[i][1])
        else :
            xcord2.append(dataIn[i][0])
            ycord2.append(dataIn[i][1])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1,ycord1,s = 30,c = 'red',marker='s')
    ax.scatter(xcord2,ycord2,s= 30,c ='green')
    # x = arange(-3.0, 3.0, 0.1)
    # print(shape(x))
    # y = (-weights[0]-weights[1]*x)/weights[2]
    # print(shape(y))
    # ax.plot(x, y.transpose())
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

def selectJrand(i,m):
    j = i
    while (j == i):
        j = int(random.uniform(0,m))
    return j

def clipAlpha(aj,L,H):
    if aj > H:
        return H
    if aj < L :
        return L
    return aj


def smoSimple(dataIn,classLabels,C,toler,maxIter):
    dataMatrix = mat(dataIn)
    labelMatrix = mat(classLabels).transpose()
    b = 0
    m,n = shape(dataMatrix)
    alpha = mat(zeros((m,1)))
    # print(labelMatrix)
    iter = 0
    while iter < maxIter:
        alphaPairChanged = 0
        for i in range(m):
            # f(xi) = sum(aj*yj*k(xj,xi)+b)
            # fXi = float(multiply(alpha,labelMatrix).T*(dataMatrix*dataMatrix[i,:].T)) + b
            # print(fXi)
            fXi = float(multiply(alpha,labelMatrix).T*(dataMatrix*dataMatrix[i,:].T)) +b
            # ei = f(xi)-yi
            Ei =fXi - float(labelMat[i])
            ## yi*Ei,why?
            uVi =  labelMatrix[i] *Ei
            ## violate KKT 
            ## choose second alpha 
            if ( uVi< -toler and alpha[i] < C) or (uVi> toler and alpha[i] > 0) :
                j =  selectJrand(i,m)
                fXj = float(multiply(alpha,labelMatrix).T*(dataMatrix*dataMatrix[j,:].T)) +b
                Ej = fXj - float(labelMatrix[j])   
                alphaIOld = alpha[i].copy()
                alphaJOld = alpha[j].copy()
                # print(alphaIOld,alphaJOld)
                ## cut value 
                L = None
                H = None
                if labelMatrix[i] != labelMatrix[j] :
                    L = max(0,alpha[j]-alpha[i])
                    H = min(C,C+alpha[j]-alpha[i])
                else :
                    L = max(0,alpha[j]+alpha[i]-C)
                    H = min(C,alpha[j]+alpha[i])
                # print ('L == H',L,H)
                if L == H :
                    print ('L == H',L,H)
                    continue

                ## k11 + k22 - 2*k12
                eta  = 2.0*dataMatrix[i,:]*dataMatrix[j,:].T - dataMatrix[i,:]*dataMatrix[i,:].T - dataMatrix[j,:] * dataMatrix[j,:].T
                
                if eta >=0 :
                    print('eta >= 0 ')
                    continue
                print(Ei,Ej)
                ## aj_new = aj_old - yj*(Ei-Ej)/eta
                alpha[j] -= labelMatrix[j] *(Ei-Ej)/eta
                alpha[j] = clipAlpha(alpha[j],L,H)
                ## 
                if (abs(alpha[j] - alphaJOld) < 0.00001):
                    print('j not moving enough',alpha[j] , alphaJOld)
                    continue
                ## ai_new = ai_old + yi*yj*(-aj_new+aj_old)
                alpha[i] += labelMatrix[i]*labelMatrix[j]*(-alpha[j]+alphaJOld)

                ## update b

                # b1_new = -Ei-yi*Kii(ai_new-ai_old) -yj*Kji*(aj_new-aj_old)+b_old
                b1 = b -Ei -labelMatrix[i]*dataMatrix[i,:]*dataMatrix[i,:].T*(alpha[i]-alphaIOld)-labelMatrix[j]*dataMatrix[i,:]*dataMatrix[j,:].T*(alpha[j]-alphaJOld)
                # b2_new
                b2 = b -Ej-labelMatrix[i]*dataMatrix[i,:]*dataMatrix[j,:].T*(alpha[i]-alphaIOld)-labelMatrix[j]*dataMatrix[j,:]*dataMatrix[j,:].T*(alpha[j]-alphaJOld)

                if alpha[i] < C and alpha[i] > 0 :
                    b = b1
                elif alpha[j] < C and alpha[i] >0:
                    b = b2
                else :
                    b = (b1+b2)/2.0
                
                alphaPairChanged +=1

                print('iter :%d ,i : %d,pairChanged :%d'%(iter,i,alphaPairChanged))

        if (alphaPairChanged == 0):
            iter += 1
        else :
            iter = 0
        
        print('iteration number : %d '%(iter))

    return b,alpha
         
            

# class OptStruct:
#     def __init__(self,dataIn,classLabels,C,toler):
#         self.X = dataIn
#         self.labelMatrix = classLabels
#         self.C = C
#         self.toler = toler
#         self.m = shape(dataIn)[0]
#         self.alpha = mat(zeros((self.m,1)))
#         self.b = 0
#         self.eCache = mat(zeros((self.m,2)))
#     def calcEk(os,k):
#         fXk = float(multiply(os.alpha,os.labelMatrix).T *(os.X*os.X[k,:].T)) +os.b
#         Ek = fXk-float(os.labelMatrix[k])
#         return Ek
#     def selectJ(i,os,Ei):


dataMat ,labelMat = loadData('testSet.txt')
# print(dataMat)
# plotBestFit(dataMat,labelMat)
b,alphas = smoSimple(dataMat, labelMat, 0.6, 0.001, 40)
print(b,alphas[alphas>0])