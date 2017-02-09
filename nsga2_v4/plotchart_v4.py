import matplotlib.pyplot as plt
import numpy as np
import csv
import math
from mymodel import rbfnetwork

data = []
speed = []
vehicle_distance = []
deviate = []
resnum  = 1

"""testing data"""

with open('train/testdata-4.csv', 'rb') as f:
    reader = csv.reader(f)
    reader.next()
    for row in reader:
        speed.append(row[3])
        vehicle_distance.append(row[4])
        deviate.append(row[5])

speed = map(float, speed)
vehicle_distance = map(float,vehicle_distance)
deviate = map(float,deviate)

vehicle_distance = np.multiply(vehicle_distance,-1)


from mymodel import featurevector
featurex = featurevector(np.array([speed,vehicle_distance,deviate]),2,1)
featurex.getbigf()
featurex.getdbigf()
featurex.getba()
featurex.getbm()
featurex = featurex.getfeaturev()



##############################################



pcount = 0
fitvres = []
best = 30000000
compromise = 100000000
bestfit = 1000000
lbestfit = bestfit
pnum = 50
errorcount = []

with open('result/v4nsga2_out_'+ str(resnum) +'.csv','rb') as f:
    reader = csv.reader(f)
    f1 = []
    f2 = []
    for row in reader:
        f1.append(float(row[0]))
        f2.append(float(row[1]))

best = []
distance = []

for i in range((len(f1)-50),len(f1)):
    best.append(np.sqrt(np.square(f1[i]) + np.square(f2[i])))
    ma = np.max(best)
    mi = np.min(best)
    if mi==ma:
        mi = 1
        ma = 0
    for index,content in enumerate(best):
        best[index] = content / np.fabs(ma-mi)

for i in range((len(f1)-50),len(f1)):
    distance.append(np.fabs(f1[i] - f2[i]))
    ma = np.max(distance)
    mi = np.min(distance)
    if mi==ma:
        mi = 1
        ma = 0
    for index,content in enumerate(distance):
        distance[index] = content / np.fabs(ma - mi)

rank = np.zeros_like(best)
for i in range(0,len(best)):
    for j in range(0,len(best)):
        if i == j:
            continue
        if best[i] < best[j]:
            rank[i] +=1

for i in range(0, len(distance)):
    for j in range(0, len(distance)):
        if i == j:
            continue
        if distance[i] < distance[j]:
            rank[i] += 1

bestindex = np.argmax(rank)

n = np.array(range(0,len(f1)))
plt.scatter(f1,f2)




# """Linear model"""
#
#
# attributes = []
# with open('result/v4res_'+ str(resnum) +'.csv', 'rb') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         attributes.append(row)
#
#
#
# n = np.array(range(0,len(f1)))
# plt.scatter(f1,f2)
# w = []
# plt.show()
# attributes[bestindex][0] = attributes[bestindex][0].split("[")[1]
# attributes[bestindex][(len(w)-1)] = attributes[bestindex][(len(w)-1)].split("]")[0]
# w = np.array(attributes[bestindex],dtype=float)
#
# def modelf(x):
#     global w
#     return np.dot(x,w)

# modelres = []
# for i in range(0,len(featurex)):
#     modelres.append(modelf(featurex[i]))

"""RBF"""


attributes = []
with open('result/v4res_'+ str(resnum) +'.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        attributes.append(row)
w = []
plt.show()
attributes[bestindex][0] = attributes[bestindex][0].split("[")[1]
attributes[bestindex][-1] = attributes[bestindex][-1].split("]")[0]
w = np.array(attributes[bestindex],dtype=float)

k_info = []
with open('result/v4res_kmeans_' + str(resnum) + '.csv', 'rb') as f:
    reader = csv.reader(f)
    reader.next()
    for row in reader:
        k_info.append(row)

for c in range(0,len(k_info)):
    k_info[c][0] = k_info[c][0].split("[")[1]
    k_info[c][-1] = k_info[c][-1].split("]")[0]


centroid = np.array(k_info[1:],dtype= float)
width = np.array(k_info[0],dtype = float)


modelres = []
for i in range(0,len(featurex)):
    modelres.append(rbfnetwork(w,width,centroid,featurex[i]))


print w
print str(f1[len(f1)-50 + bestindex]) +'......'+ str(f2[len(f1)-50+bestindex])
print bestindex
import matplotlib.pyplot as plt2
plt2.plot(modelres)
plt2.ylabel('result')
plt2.show()


