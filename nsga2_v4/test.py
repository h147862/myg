import numpy as np
from sklearn.cluster import KMeans
from run_nsga2_v4 import featurevector
import csv
from sklearn.metrics import silhouette_score


speed = []
vehicle_distance = []
deviate = []
deltaf = []

with open('train/testdata-3.csv', 'rb') as f:
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








# def sigmoid(x):
#     return 1/(1+np.exp(-0.1*(x-100)))
#
#
#
#
# print sigmoid(102)



def rbfnetwork(a,center,x):
    temp = 0
    for i in len(a):
        temp = temp + a[i] * np.power(np.linalg.norm(np.subtract(x,center[i])),2)
    return temp


featurex = featurevector(np.array([speed,vehicle_distance,deviate]),2,1)
featurex.getbigf()
featurex.getdbigf()
featurex.getba()
featurex.getbm()
featurex = featurex.getfeaturev()


num_of_testing = 495
# clusterscore = np.zeros_like(range(num_of_testing))
# for num_of_group in range(1,(num_of_testing+1)):
#     kmeans = KMeans(n_clusters=num_of_group, random_state=0).fit(featurex)
#     group = [list() for i in range(num_of_group)]
#     for index , content in enumerate(kmeans.labels_):
#         for i in range(num_of_group):
#             if content == i:
#                 group[content].append(index)
#
#
#     for index,content in enumerate(group):
#         for i in content:
#             clusterscore[(num_of_group-1)] += np.linalg.norm(kmeans.cluster_centers_[index] - featurex[content])
#
# print clusterscore








# num_of_group = len(featurex)
# temp = 0
# kmeans = KMeans(n_clusters=num_of_group, random_state=0).fit(featurex)
# group = [list() for i in range(num_of_group)]
# for index , content in enumerate(kmeans.labels_):
#     for i in range(num_of_group):
#         if content == i:
#             group[content].append(index)
#
#
# for index,content in enumerate(group):
#     for i in content:
#         temp += np.linalg.norm(kmeans.cluster_centers_[index] - featurex[content])
#
# print temp




