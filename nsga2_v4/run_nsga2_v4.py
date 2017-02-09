import  numpy as np
import csv
from mymodel import featurevector , rbfnetwork , getgaussianwidth
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from nsga2_v4 import respath,kmeanpath



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
# width = 2
# step = 1
#
# f = np.array([speed,vehicle_distance,deviate])


featurex = featurevector(np.array([speed,vehicle_distance,deviate]),2,1)
featurex.getbigf()
featurex.getdbigf()
featurex.getba()
featurex.getbm()
featurex = featurex.getfeaturev()



"""kmneans tune k."""


score = -5
range_of_k = [10,200]
for k in range(range_of_k[0],range_of_k[1]):
    temp = KMeans(n_clusters=k,random_state=0).fit(featurex)
    tempscore = silhouette_score(featurex, temp.labels_)
    if score < tempscore:
        score = tempscore
        kmeans = temp

number_of_k = len(kmeans.cluster_centers_)
gaussian_width = getgaussianwidth(kmeans.cluster_centers_)

kresult = open( kmeanpath , 'w')
kresult.write(str(number_of_k) + '\n')
kresult.write(str(gaussian_width) + '\n')
for centroid in kmeans.cluster_centers_:
    kresult.write(str(list(centroid)) + '\n')
kresult.close()


print number_of_k

"""set maxima score."""

# maxdangerscore = 0
# for i in range(0,len(featurex)):
#     maxdangerscore += 0.5 * np.linalg.norm(featurex[i])
# maxdangerscore = maxdangerscore / len(featurex)

maxdangerscore = 100
maximun_coeficient = 20



labelindex = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,488,489,490,491,492,493,494]
bs = []
lambdac = 1
lbf = []

for i in range(0,30):
    if i < 23:
        bs.append(0)
    else:
        bs.append(maxdangerscore)

res = []

gennum = 500


'''
Created on 10/01/2011

@author: 04610922479
'''
import random
from nsga2_v4 import Solution
from nsga2_v4 import NSGAII


crossindex = [1,2,4]





class T1Solution(Solution):
    '''
    Solution for the T1 function.
    '''
    def __init__(self):
        '''
        Constructor.
        '''
        Solution.__init__(self, 2)

        self.xmin = 0.0
        self.xmax = 1.0
        self.arsum = 0

        """W for Linear model."""

        # w = []
        # for i in range(0,len(featurex[0])):
        #     w.append(random.uniform(0,maximun_coeficient))
        # self.attributes = w

        """W for RBFnetwork."""


        w = []
        for i in range(len(kmeans.cluster_centers_)):
            w.append(random.uniform(0,maximun_coeficient))
            self.attributes = w
            # self.r = random.random()
            # self.r = 0.2

    def object1(self):

        """ Fitness function 1 ."""

        """For Linear model."""


        # res = []
        # for i in labelindex:
        #     res.append(np.dot(featurex[i], self.attributes))
        # lmodelres = np.array(res)
        # return np.linalg.norm(bs - lmodelres)

        """For RBF."""


        res = []
        for i in labelindex:
            res.append(rbfnetwork(self.attributes,gaussian_width,kmeans.cluster_centers_,featurex[i]))
        return np.sum(res)




    def object2(self):
        """ Fitness function 2 ."""

        """For Linear model."""


        # res = []
        # for i in range(0, len(featurex)):
        #     res.append(np.dot(featurex[i], self.attributes))
        # modelres = np.array(res)
        # temp = 0
        # for i in range(0,1):
        #     for j in range(0,(len(modelres)-1)):
        #         temp = temp + (modelres[j]-modelres[(j+1)])*(modelres[j]-modelres[(j+1)])
        # return temp

        """For RBF."""


        res = []
        for i in range(0, len(featurex)):
            res.append(rbfnetwork(self.attributes,gaussian_width,kmeans.cluster_centers_,featurex[i]))
            temp = 0
        for i in range(0,1):
            for j in range(0,(len(res)-1)):
                temp = temp + (res[j]-res[(j+1)])*(res[j]-res[(j+1)])
        return temp






    def evaluate_solution(self):
        '''
        Implementation of method evaluate_solution() for T1 function.
                 '''

        self.objectives[0] = self.object1()
        self.objectives[1] = self.object2()



    def crossover(self, other):
        '''
        Crossover of T1 solutions.
        '''

        """For Linear model."""

        # child_solution = T1Solution()
        #
        # child_solution.attributes = self.attributes[:]
        # for index in crossindex:
        #     child_solution.attributes[index] = other.attributes[index]
        # return child_solution

        """For RBF."""

        child_solution = T1Solution()
        child_solution.attributes = self.attributes[:]
        for index in crossindex:
            child_solution.attributes[index] = other.attributes[index]
        return child_solution

    def mutate(self):
        '''
        Mutation of T1 solution.
        '''

        """For Linear model."""
        # self.attributes[random.randint(0, 4)] = random.random()
        """For RBF."""
        self.attributes[random.randint(0,len(kmeans.cluster_centers_)-1)] = random.uniform(0,maximun_coeficient)

if __name__ == '__main__':
    nsga2 = NSGAII(2, 0.1, 1.0)

    P = []
    for i in range(50):
        P.append(T1Solution())

    nsga2.run(P,50,gennum)

    # csv_file = open('C:/Users/T/Desktop/nsga2.tar/nsga2/nsga2/nsga2_out.csv', 'w')
    # res_file = open('C:/Users/T/Desktop/nsga2.tar/nsga2/nsga2/v3res.csv', 'w')
    res_file = open(respath, 'w')



    for i in range(len(nsga2.P)):
        # csv_file.write("" + str(P[i].objectives[0]) + ", " + str(P[i].objectives[1])+ ","+ str(P[i].attributes) + "\n")
        res_file.write("" + str(nsga2.P[i].attributes) + "\n")
    # csv_file.close()
    res_file.close()

    print res



