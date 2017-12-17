from numpy import *
import matplotlib.pyplot as plt

def loadSimpleData():
    dataMat = matrix([[1.0, 2.1],
                      [2.0, 1.1],
                      [1.3, 1.0],
                      [1.0, 1.0],
                      [2.0, 1.0]
                      ])
    classLabel = [1.0, 1.0, -1.0, -1.0, 1.0]
    return dataMat,classLabel

def stumpClassfiy(dataIn,dimen,threshVal,threshIneq):
    # print(dataIn)
    retArray = ones((shape(dataIn)[0],1))
    # print(retArray)
    # print(threshVal)
    if threshIneq =='lt':
        retArray[dataIn[:,dimen]<=threshVal]=-1.0
    else:
        retArray[dataIn[:,dimen]> threshVal]=-1.0
    # print(retArray)
    return retArray

def buildStump(dataIn,classLabels,D):
    dataMatrix = mat(dataIn)
    labelMatrix=mat(classLabels).T
    m,n = shape(dataMatrix)
    numSteps = 10.0
    bestStump={}
    bestClassEast= mat(zeros((m,1)))

    minError = inf
    for i in range(n):
        rangeMin = dataMatrix[:,i].min()
        rangeMax = dataMatrix[:,i].max()
        stepSize = (rangeMax-rangeMin)/numSteps
        # print(i)
        for j in range(-1,int(numSteps)+1):
            for inequal in ['lt','gt']:
                threshVal =(rangeMin+float(j)*stepSize)
                predictedVals = stumpClassfiy(dataMatrix,i,threshVal,inequal)
                errArr = mat(ones((m,1)))
                # print('predictedVals: ' , predictedVals)
                errArr[predictedVals==labelMatrix]=0
                weightedError = D.T*errArr
                # print ("split: dim %d, thresh %.2f, thresh ineqal: %s, the weighted error is %.3f" %(i, threshVal, inequal, weightedError))
                if weightedError < minError:
                    minError = weightedError
                    bestClassEast = predictedVals.copy()
                    bestStump['dim'] = i
                    bestStump['thresh'] = threshVal
                    bestStump['ineq'] = inequal
    return bestStump,minError,bestClassEast


def adaboost(dataIn,classLabels,numIt = 40):
    weakClassArr =[]
    m ,n = shape(dataIn)
    D = mat(ones((m,1))/m)
    aggClassEst = mat(zeros((m,1)))

    for i in range(numIt):
        stump,error,classEast = buildStump(dataMatrix,labelClass,D)
        print("D:",D.T)
        # am = 1/2*log((1-em)/em)
        alpha = float(0.5*log((1.0-error)/max(error,1e-16)))
        stump['alpha'] = alpha
        weakClassArr.append(stump)
        print('est :',classEast.T )
        ## exp(-am*yi*Gm(xi))
        # print(alpha)
        # print(classEast)
        # print(mat(classLabels))
        expon = multiply(-1*alpha*mat(classLabels).T,classEast)
        D = multiply(D,exp(expon))
        D = D/D.sum()

        ## am*Gm(x)
        aggClassEst += alpha*classEast
        print('aggClassEst: ',aggClassEst)

        ## sign(x) -1 if x < 0 ,0 if x ==0, 1 if x > 0
        aggErrors = multiply(sign(aggClassEst) != mat(classLabels).T,ones((m,1)))
        errRate = aggErrors.sum()/m

        print("total error :" ,errRate)

        if errRate == 0:
            break

    return weakClassArr



def drawData(dataIn,labelIn):
    xRecord1=[]
    yRecord1=[]
    xRecord2=[]
    yRecord2=[]

    m,n = shape(dataIn)
    print(m,n)
    for i in range(m):
        if labelIn[i] == 1.0:
            # print(dataIn[i,0])
            xRecord1.append(dataIn[i,0])
            yRecord1.append(dataIn[i,1])
        else :
            xRecord2.append(dataIn[i,0])
            yRecord2.append(dataIn[i,1])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xRecord1,yRecord1,c='r',marker='o')
    ax.scatter(xRecord2,yRecord2,c='b',marker='x')
    plt.show()

dataMatrix ,labelClass = loadSimpleData()
# drawData(dataMatrix,labelClass)
m,n = shape(dataMatrix)
D = mat(ones((m,1))/5)
# 
# print(dataMatrix)
# bestStump,minError,bestClassEast = buildStump(dataMatrix,labelClass,D)

# print(bestStump)
# print(minError)
# print(labelClass)
weakClassArr = adaboost(dataMatrix,labelClass)
print(weakClassArr)