import numpy as np




class featurevector():
    def __init__(self,rawdata,width,stepsize):
        self.f = rawdata
        self.width = width
        self.stepsize = stepsize
    def getbigf(self):
        res = []
        for i in range(0,len(self.f)):
            temp = []
            for j in range(self.width,len(self.f[i])):
                temp.append(self.f[i][(j-self.width):j])
            res.append(temp)
        self.bf = np.asarray(res)

    def getdbigf(self):
        res = []
        for i in range(0,len(self.bf)):
            temp2 = []
            for j in range(0,(len(self.bf[i])-1)):
                temp = []
                for k in range(0,(len(self.bf[i][j])-1)):
                    temp.append((self.bf[i][j][(k+1)] - (self.bf[i][j][(k)])))
                temp2.append(temp)
            res.append(temp2)
        self.dbf =  np.asarray(res)


    def getbg(self):
        res = []
        temp = []
        for j in range(0,(len(self.dbf[1])-1)):
            temp1 = (np.sum(self.db[0][(j + 1)] - self.db[0][j])) / self.width
            temp2 = (np.sum(self.db[1][(j + 1)] - self.db[1][j])) / self.width
            temp3 = (np.sum(self.db[2][(j + 1)] - self.db[2][j])) / self.width
            temp = np.array([temp1,temp2,temp3])
            res.append(temp)
        self.bg = np.asarray(res)

    def getbm(self):
        bm = []
        for i in range(self.width, len( self.bf[1])):
            temp = np.array([np.max(self.bf[0][(i - self.width):i]), np.max(self.bf[1][(i - self.width):i])])
            bm.append(temp)
        self.bm = np.asarray(bm)

    def getba(self):
        ba = []
        for i in range(self.width, len(self.bf[1])):
            temp = np.array(
                [np.mean(self.dbf[0][(i - self.width):i]), np.mean(self.dbf[1][(i - self.width):i]), np.mean(self.dbf[2][(i - self.width):i])])
            ba.append(temp)
        self.ba = np.asarray(ba)


    def getfeaturev(self):
        res = []
        input = []
        input.append(self.bm)
        input.append(self.ba)
        for i in range(0,len(input[1])):
            temp = []
            for j in range(0,len(input)):
                temp.append(input[j][i])
            temp = np.hstack(temp)
            res.append(temp)
        return np.asarray(res)




def getgaussianwidth(centroid):
    r = 2       # r-nearest neighbours
    res = []
    distence = []
    nearest = []
    for c in centroid:
        for rest in centroid:
            if sum(c != rest) == 0:
                continue
            distence.append(np.power(np.linalg.norm(np.subtract(c,rest)),2))
        for j in range(r):
            minima = np.min(distence)
            nearest.append(minima)
            distence.remove(minima)
        res.append(np.sqrt(np.sum(nearest)) / r)
    return res




def rbfnetwork(coefficient,r,centroid,x):
    temp = 0
    for i in range(len(coefficient)):
        temp = temp + coefficient[i] *  np.exp(-1 * (np.power(np.linalg.norm(np.subtract(x,centroid[i])),2) / r[i]))
    return temp





