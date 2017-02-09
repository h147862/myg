import numpy as np
import csv

data = []
speed = []
vehicle_distance = []
deviate = []
newf = []
deltaf = []
tw = 2
ts = 1


def emulti(x):
    return  round(x*x,5)


def vectorsquare(x):
    res = []
    for i in range(0,len(x)):
        res.append(map(emulti,x[i][:]))
    return res

def getbigf(x):
    res = []
    for i in range(0, (len(x[0])- (tw-1)), ts):
        if len(x[0]) < (i + ts):
            break
        temp = []
        for j in range(0,(len(x))):
            temp.append(x[j][i:(i+tw)])
        res.append(temp)
    return res


def getzcr(x,index):
    res = 0
    temp = []
    for i in range(0,len(x)):
        for j in range(0,len(x[0][0])):
            temp.append(x[i][0][j])
    for i in range(1,len(temp)):
        res = res + (temp[i][index]-temp[i-1][index])
    return res / (len(temp)-1)



def getmaxf(x):
    res = []
    for i in range(0,len(x)):
        temp = []
        for j in range(0,len(x[0])):
            maxf = x[i][j][0]
            for k in range(1,(len(x[0][0]))):
                maxf = np.maximum(maxf,x[i][j][k])
            temp.append(maxf)
        res.append(temp)
    return res


def getminf(x):
    res = []
    for i in range(0,len(x)):
        temp = []
        for j in range(0,len(x[0])):
            minf = x[i][j][0]
            for k in range(1,(len(x[0][0]))):
                minf = np.minimum(minf,x[i][j][k])
            temp.append(minf)
        res.append(temp)
    return res


def getmeanf(x):
    res = []
    for i in range(0,len(x)):
        temp = []
        for j in range(0,len(x[0])):
            temp.append(np.sum(x[i][j],axis= 0)/len(x[0][0]))
        res.append(temp)
    return res


def getstd(x,m):
    res = []
    for i in range(0,len(x)):
        temp2 = []
        for j in range(0,len(x[0])):
            temp = []
            for k in range(0,len(x[0][0])):
                temp.append(x[i][j][k] - m [i][j])
            temp = np.sum(np.square(temp),axis=0)
            temp = np.sqrt(temp / len(x[0][0]))
            temp2.append((temp/len(x[0][0])))
        res.append(temp2)
    return res

def getfeaturev(maxf,minf,meanf,std):
    res = []
    temp = []
    for i in range(0,len(maxf)):
        temp = []
        for j in range(0,len(maxf[0])):
            for k in range(0,len(maxf[0][0])):
                temp.append(maxf[i][j][k])
            for k in range(0, len(minf[0][0])):
                temp.append(minf[i][j][k])
            for k in range(0, len(meanf[0][0])):
                temp.append(meanf[i][j][k])
            for k in range(0, len(std[0][0])):
                temp.append(std[i][j][k])
        res.append(temp)
    return res


with open('testdata.csv', 'rb') as f:
    reader = csv.reader(f)
    realdata = reader.next()
    for row in reader:
        speed.append(row[3])
        vehicle_distance.append(row[4])
        deviate.append(row[5])

speed = map(float, speed)
vehicle_distance = map(float,vehicle_distance)
deviate = map(float,deviate)



f = np.array([speed,vehicle_distance,deviate])
f = f.transpose()

for i in range(0,f.shape[0]):
    temp = np.subtract(map(float,f[i+1][:]),map(float,f[i][:]))
    deltaf.append(temp)
    if i == (f.shape[0]-2):
        temp = np.subtract(map(float, f[i + 1][:]), map(float, f[i][:]))
        deltaf.append(temp)
        break

newf = [f,np.asarray(deltaf),np.asarray(vectorsquare(f)),np.asarray(vectorsquare(deltaf))]
bigf = getbigf(newf)


maxf = getmaxf(bigf)
minf = getminf(bigf)
mf = getmeanf(bigf)
std = getstd(bigf,mf)
featurex = getfeaturev(maxf,minf,mf,std)





def mycostfun(w):
    global featurex
    global lambdac
    global scorey
    global labeledx
    global L
    scoreyt = np.transpose(scorey)

    res = []
    for i in range(0, len(labeledx)):
        res.append(np.dot(labeledx[i], w))
    lmodelres = np.array(res)
    lmodelrest = np.transpose(lmodelres)

    res = []
    for i in range(0, len(featurex)):
        res.append(np.dot(featurex[i], w))
    modelres = np.array(res)
    modelrest = np.transpose(modelres)

    res = np.dot(scoreyt, scorey) - 2 * np.dot(scoreyt, lmodelres) + np.dot(lmodelrest, lmodelres) + 2 * lambdac * np.dot(np.dot(modelrest, L), modelres)
    return res





def mycostfun_der(w):
    global featurex
    global lambdac
    global scorey
    global labeledx
    global L
    scoreyt = np.transpose(scorey)
    labeledxt = np.transpose(labeledx)
    temp = []
    for i in range(len(labeledx)):
        temp.append(labeledx[i][1])
    newlabeledx = np.array(temp)
    newlabeledxt = np.transpose(newlabeledx)

    temp = []

    for i in range(len(featurex)):
        temp.append(featurex[i][1])
    newfeaturex = np.array(temp)
    res =  np.dot(scoreyt,newlabeledx) + 2* w*np.dot(newlabeledxt,newlabeledx) + 4 * lambdac * w*np.dot(np.dot(np.transpose(newfeaturex),L),newfeaturex)

    return res




labelindex = [0,1,35,36,37,38,39]
w = []
labeledx = []
scorey = []
lambdac = 1
lbigf = []


for i in range(0,48):
    w.append(1)

for i in range(0,7):
    if i < 2:
        scorey.append(0)
    else:
        scorey.append(300)


for i in labelindex:
    lbigf.append(bigf[(i-1)])


lmaxf = getmaxf(lbigf)
lminf = getminf(lbigf)
lmf = getmeanf(lbigf)
lstd = getstd(lbigf,lmf)
labeledx = getfeaturev(lmaxf,lminf,lmf,lstd)


def gets(x):
    res = np.zeros((len(x),len(x)))
    for i in range(0,len(x)):
        for j in range(0,len(x)):
            if i!=j:
                # index = ((i*j)+j)
                # res[index] = np.square(sum(np.subtract(x[j],x[i]))*-1/1.25)
                res[i][j] = np.square(sum(np.subtract(x[j], x[i])) * -1 / 1.25)
    return res



def getl(x):
    res = x
    for i in range(0,x.shape[1]):
        temp = sum(x[i][:])
        res[i,i] = temp
    return res

S = gets(featurex)
L = getl(S)

w = [0.15447159074352323, 0.8737248987905283, 0.5481063266778256, 0.36704981433538375, 0.6290635559630787, 0.6872603467383318, 0.3528217024371251, 0.9583313767130082, 0.999059276976836, 0.14710691621277305, 0.7883377031972135, 0.8821430413084758, 0.27606067498863884, 0.5207228664609977, 0.02910239574743223, 0.03309437744618238, 0.4966775576286643, 0.9583736358433194, 0.4938671249116423, 0.16489970949099098, 0.9047423151900985, 0.6502046771782775, 0.7550100982325446, 0.6556949261063221, 0.127697955302306, 0.9800752527235012, 0.6485054670630419, 0.17517249144708236, 0.8951303877257741, 0.35902893624175847, 0.1474206864946811, 0.5785292791900946, 0.9320678378666482, 0.5103119136129002, 0.6612015325098884, 0.559854024722979, 0.10641639673378844, 0.6287084400946057, 0.14202198140285838, 0.9350508379145488, 0.028888427346635992, 0.28352211806993544, 0.6334944815554149, 0.6645714994560306, 0.5907803648332621, 0.4524097840214709, 0.7113099685024313, 0.16841489161187662]



def safetyindex(x):
    return np.dot(x,w)





print "{0:.60f}".format(mycostfun(w))

res = []
for i in range(0,len(featurex)):
    res.append(safetyindex(featurex[i]))

import matplotlib.pyplot as plt


print res




plt.plot(res)
plt.ylabel('some numbers')
plt.show()

