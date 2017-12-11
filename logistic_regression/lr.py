import numpy as np
import matplotlib.pyplot as plt

def sigmoid(x):
    return(1 / (1 + np.exp(-x)))


def loadDataSet(fn):
    dataMat = []
    labelMat = []
    fr = open(fn)
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat, labelMat


def gradAscent(dataIn, labelIn):
    dataMatrix = np.mat(dataIn)
    labelMatrix = np.mat(labelIn).transpose()
    m, n = np.shape(dataMatrix)
    alpha = 0.001
    maxCycles = 500
    weights = np.ones((n, 1))
    for k in range(maxCycles):
        h = sigmoid(dataMatrix * weights)
        error = (labelMatrix - h)
        weights = weights + alpha * dataMatrix.transpose() * error
    return weights


def plotBestFit(dataIn, labelIn, weights):
    n = np.shape(dataIn)[0]
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
    x = np.arange(-3.0, 3.0, 0.1)
    print(np.shape(x))
    y = (-weights[0]-weights[1]*x)/weights[2]
    print(np.shape(y))
    ax.plot(x, y.transpose())
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

x, y = loadDataSet('test.txt')
# print(x[0:1])
weight = gradAscent(x, y)

# index =
print(np.shape(x),np.shape(y))
plotBestFit(np.array(x),y,weight)
# m, n = np.shape(x)
# for i in range(m):
#     print(y[i], sigmoid(x[i] * weight)[0] > 0.5)

# print(sigmoid(0))
