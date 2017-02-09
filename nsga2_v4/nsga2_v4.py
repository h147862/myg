
'''
Created on 07/01/2011

@author: 04610922479
'''

import sys
import random
import math
import os
import numpy as np



dirpath = os.getcwd() + '/result'
if not os.path.exists(dirpath):
    os.mkdir(dirpath)

testrpath = dirpath + '/v4res_'
testopath = dirpath +  '/v4nsga2_out_'


numberoffile = 1

while os.path.isfile(testrpath + str(numberoffile) + '.csv' ):
    numberoffile += 1

respath = testrpath + str(numberoffile) + '.csv'
outpath = testopath + str(numberoffile) + '.csv'
kmeanpath = os.getcwd() + '/result/v4res_kmeans_' + str(numberoffile) + '.csv'

if os.path.isfile(outpath):
    os.remove(outpath)




class Solution:
    '''
    Abstract solution. To be implemented.
    '''

    def __init__(self, num_objectives):
        '''
        Constructor. Parameters: number of objectives.
        '''
        self.num_objectives = num_objectives
        self.objectives = []
        for _ in range(num_objectives):
            self.objectives.append(None)
        self.attributes = []
        # self.rank = sys.maxint
        self.distance = 0.0

    def evaluate_solution(self):
        '''
        Evaluate solution, update objectives values.
        '''
        raise NotImplementedError("Solution class have to be implemented.")

    def crossover(self, other):
        '''
        Crossover operator.
        '''
        raise NotImplementedError("Solution class have to be implemented.")

    def mutate(self):
        '''
        Mutation operator.
        '''
        raise NotImplementedError("Solution class have to be implemented.")

    def __rshift__(self, other):
        '''
        True if this solution dominates the other (">>" operator).
        '''
        dominates = False

        for i in range(len(self.objectives)):
            if self.objectives[i] > other.objectives[i]:
                return False

            elif self.objectives[i] < other.objectives[i]:
                dominates = True

        return dominates

    def __lshift__(self, other):
        '''
        True if this solution is dominated by the other ("<<" operator).
        '''
        return other >> self


# def crowded_comparison(s1, s2):
#     '''
#     Compare the two solutions based on crowded comparison.
#     '''
#     if s1.distance  > s2.distance:
#         return 1
#     else:
#         return 0


class NSGAII:
    '''
    Implementation of NSGA-II algorithm.
    '''
    current_evaluated_objective = 0

    def __init__(self, num_objectives, mutation_rate=0.1, crossover_rate=1.0):
        '''
        Constructor. Parameters: number of objectives, mutation rate (default value 10%) and crossover rate (default value 100%).
        '''
        self.num_objectives = num_objectives
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        random.seed();

    def processpop(self, inum):

        for j in self.P:
            self.csv_file.write("" + str(j.objectives[0]) + ", " + str(j.objectives[1]) + "," + str(
                j.objectives[0] + j.objectives[1]) + str(j.objrank) + ',' +str(j.num_of_child) +"\n")

        print "Iteracao ", inum, "-----", self.best, "......", self.bobj0, "......", self.bobj1
        # print "Iteracao ", inum, "-----", self.best, "......", self.bobj0, "......", self.bobj1,number_of_k

        """First 1/4 part of the generation choosen by comparing compromiserank,and the rest parts by comparing both objrank and crowdingrank"""


        # R = []
        # R.extend(self.P)
        # R.extend(self.Q)
        # self.getrank(R)
        # self.getcomprmise(R)
        # self.sortcomrank(R)
        # temp = R[0:int(np.floor(len(R)*0.25))]      #first part
        # temp2 = list(set(R) - set(temp))            #rest part
        #
        # self.getrank(temp2)
        # self.crowding_distance_assignment(temp2)
        # self.sort_crowding(temp2)
        #
        #
        # del self.P[:]
        #
        # self.P.extend(temp)
        # # self.P.extend(temp2[0:int(self.population_size - np.floor(len(R) * 0.25))])
        # self.P.extend(temp2)
        # if len(self.P) > self.population_size:
        #     del self.P[self.population_size:]
        # self.Q = self.make_new_pop(self.P)

        """compromiserank only"""


        R = []
        R.extend(self.P)
        R.extend(self.Q)
        self.getrank(R)
        self.getcomprmise(R)
        self.sortcomrank(R)
        # self.sortrank(R)

        del self.P[:]
        self.P.extend(R)
        if len(self.P) > self.population_size:
            del self.P[self.population_size:]
        self.Q = self.make_new_pop(self.P)



    def run(self,P, population_size, num_generations):
        '''
        Run NSGA-II.
        '''
        for s in P:
            s.evaluate_solution()
            s.objrank = 0
            s.num_of_child = 0
        self.num_generations = num_generations
        self.population_size = population_size
        self.P = P
        self.Q = []
        self.best = (P[0].objectives[0] + P[0].objectives[1])
        self.bobj0 = P[0].objectives[0]
        self.bobj1 = P[0].objectives[1]
        self.lbest = 5000000
        self.csv_file = open(outpath, 'a')

        # for i in range(0,100):
        #     self.processpop(i)
        #
        # for i in range(101, num_generations):
        #         self.processpop(i)

        for i in range(0, num_generations):
            self.processpop(i)

    def sort_objective(self, P, obj_idx):

       for i in range(0,(len(P)-1)):
           for j in range(0,(len(P)-1-i)):
               s1 = P[j]
               s2 = P[(j+1)]

               if s1.objectives[obj_idx] < s2.objectives[obj_idx]:
                   self.objmin = s1.objectives[obj_idx]
                   P[j] = s2
                   P[(j+1)] = s1
               else:
                   self.objmax = s1.objectives[obj_idx]
           if (self.objmax == self.objmin):
               self.objmax = self.objmin + 1

        # for i in range((len(P)-1), -1, -1):
        #     for j in range(1,(i+1)):
        #         s1 = P[j - 1]
        #         s2 = P[j]
        #         if s1.objectives[obj_idx] > s2.objectives[obj_idx]:
        #             self.objmax = s1.objectives[obj_idx]
        #             P[j - 1] = s2
        #             P[j] = s1
        #         else:
        #             self.objmin = s1.objectives[obj_idx]
        # if (self.objmax == self.objmin):
        #     self.objmax = self.objmin + 1

    def sort_crowding(self, P):
        for i in range(0, len(P) - 1):
            for j in range(0, len(P) - 1 - i):
                if P[j].crowdingrank > P[(j+1)].crowdingrank:
                    s1 = P[j]
                    s2 = P[(j+1)]
                    P[j] = s2
                    P[(j+1)] = s1


    # def partialorder(self, p, q):
    #     count = 0
    #     for i in range(len(p.objectives)):
    #         if (p.objectives[i] > q.objectives[i]):
    #             return 0
    #         else:
    #             count += (p.objectives[i] < q.objectives[i])
    #     if (count == 0):
    #         return 0
    #     else:
    #         return 1

    def getrank(self,p):
        for s in p:
            s.objrank = 0
        for objindex in range(0,self.num_objectives):
            for i in p:
                for j in p:
                    if i == j:
                        continue
                    if i.objectives[objindex] > j.objectives[objindex]:
                        i.objrank += 1

    def getcomprmise(self,p):
        for s in p:
            s.comrank = 0
        for i in p:
            for j in p:
                if i == j:
                    continue
                if np.fabs((i.objectives[0]-i.objectives[1])) > np.fabs((j.objectives[0]-j.objectives[1])):
                    i.comrank += 1

    def sortrank(self,p):
        for i in range(0,(len(p)-1)):
            for j in range(0,(len(p)-1-i)):
                if p[j].objrank > p[(j+1)].objrank:
                    s1 = p[j]
                    s2 = p[(j+1)]
                    p[j] = s2
                    p[(j+1)] = s1

    def sortcomrank(self,p):
        for s in p:
            s.comrank += s.objrank
        for i in range(0, (len(p) - 1)):
            for j in range(0, (len(p) - 1 - i)):
                if p[j].comrank > p[(j+1)].comrank:
                    s1 = p[j]
                    s2 = p[(j + 1)]
                    p[j] = s2
                    p[(j + 1)] = s1



    # def calculatear(self,a,b):
    #     ar = 0
    #     for i in range(0,self.num_objectives):
    #         if a.objectives[i] < b.objectives[i]:
    #             ar += 1
    #         elif a.objectives[i] > b.objectives[i]:
    #             ar += -1
    #     return ar

    def make_new_pop(self, P):
        '''
        Make new population Q, offspring of P.
        '''
        Q = []
        parent = P


        for s in P:
            s.num_of_child = 0
        # weight = np.array([np.full(25,2),np.full(25,3)])
        # weight = np.hstack(weight)
        #
        # pool = []
        # pool.append(P[0:25])
        # pool.append(P[0:25])
        # pool.append(P[25:50])
        # pool.append(P[25:50])
        # pool.append(P[25:50])
        # pool = np.hstack(pool)


        while len(Q) != len(P):
            selected_solutions = [None, None]
            while selected_solutions[0] == selected_solutions[1]:
                for i in range(2):
                    s1 = random.choice(P)
                    # s1 = random.choice(pool)
                    s2 = s1
                    while s1 == s2:
                        s2 = random.choice(P)
                        # s2 = random.choice(pool)
                    if s1.objrank < s2.objrank:
                        selected_solutions[i] = s1
                    else:
                        selected_solutions[i] = s2
                # selected_solutions[0] = s1
                # selected_solutions[1] = s2


            if random.random() < self.crossover_rate:
                child = selected_solutions[0].crossover(selected_solutions[1])
                if random.random() < self.mutation_rate:
                    child.mutate()
                child.evaluate_solution()
                if len(Q) > 0:
                    for s in Q:
                        if ((child.objectives[0] + child.objectives[1]) == (s.objectives[0] + s.objectives[1])):
                            if child.objectives[0] == s.objectives[0]:
                                selected_solutions = [None, None]

                for s in parent:
                    if (child.objectives[0] + child.objectives[1]) == (s.objectives[0] + s.objectives[1]):
                        if child.objectives[0] == s.objectives[0]:
                            selected_solutions = [None, None]

                if not selected_solutions == [None, None]:
                    s1.num_of_child += 1
                    s2.num_of_child += 1
                    Q.append(child)
        return Q




    def crowding_distance_assignment(self, p):
        '''
        Assign a crowding distance for each solution in the front.
        '''
        for s in p:
            s.crowdingrank = 0
        for obj_index in range(self.num_objectives):
            self.sort_objective(p,obj_index)
            p[0].distance = float('inf')
            p[(len(p)-1)].distance = float('inf')
            for i in range(1, (len(p)-1)):
                p[i].distance += (np.fabs(p[(i+1)].objectives[obj_index] - p[(i-1)].objectives[obj_index])) / math.fabs(self.objmax - self.objmin)

        for i in p:
            for j in p:
                if i==j:
                    continue
                if i.distance < j.distance:
                    i.crowdingrank += 1

        for i in p:
            i.crowdingrank +=i.objrank




