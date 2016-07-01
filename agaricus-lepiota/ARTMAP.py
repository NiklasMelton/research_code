#Author: Niklas Melton
#Date: 09/02/2016
#Online FuzzyARTMAP implemention.

import numpy as np, FuzzyART as ART


class ARTMAP:
    def __init__(self,rho,alpha,beta,wA=None,wB=None,wMap = None):
        self.rho = rho
        self.alpha = alpha
        self.beta = beta
        self.map = wMap
        self.A = ART.ARTnet(rho,alpha,beta,wA)
        self.B = ART.ARTnet(rho,alpha,beta,wB)


    def supervised(self, dataA, dataB):
        mapped = False
        while(not(mapped)):
  
            #determine which ART A and B clusters match the data
            clusterA = self.A.learnRun(dataA)
            clusterB = self.B.learnRun(dataB)

            if self.map is None:
                #initialize map weights if none exist
                self.map = np.zeros((self.A.clustNum, self.B.clustNum))

            #if the chosen cluster exists outside of map weight space, expand
            #the map weights to fit the new clusters
            if clusterA > (len(self.map)-1):
                z = np.zeros(len(self.map[0]))
                self.map = np.vstack((self.map,z))
                
            if clusterB > (len(self.map[0])-1):
                z = np.zeros((len(self.map),1))
                self.map = np.concatenate((self.map,z), 1)

            #check map 
            if not(np.any(self.map[clusterA] > 0)):
                self.map[clusterA][clusterB] = 1
                mapped = True
             #match tracking   
            elif self.map[clusterA][clusterB] != 1:
                Ax = np.concatenate((dataA, 1-dataA))
                self.A.rho = (ART.norm(ART.fuzzyAnd(Ax, self.A.w[clusterA]))/ART.norm(Ax)) + 0.01
            else:
                mapped = True
                
            
        self.A.rho = self.rho


    def unsupervised(self, dataA):
        #identify cluster
        clusterA = self.A.learnRun(dataA)
        clusterA2 = None
        clusterB2 = None
        #if the chosen cluster exists outside of map weight space, expand
        #the map weights to fit the new clusters
        if clusterA > (len(self.map)-1):
            z = np.zeros(len(self.map[0]))
            self.map = np.vstack((self.map,z))
            z = np.zeros((len(self.map),1))
            self.map = np.concatenate((self.map,z), 1)
            self.map[clusterA][(len(self.map[clusterA])-1)] = 1
            #find which cluster would have won previously
            clusterA2 = self.A.run(dataA, 2)
            #find B cluster for next best guess if new cluster was formed
            clusterB2 = np.argmax(self.map[clusterA2])
        #find corresponding B cluster from map
        clusterB = np.argmax(self.map[clusterA])

        return [clusterB, clusterB2]

    def runForward(self, dataA):
        clusterA = self.A.run(dataA)
        clusterB = np.argmax(self.map[clusterA])
        if (len(self.B.w.shape) == 1 and clusterB == 0):
            dataB =  self.B.w
        else:
            dataB =  self.B.w[clusterB]
        dataB = dataB[:len(dataB)/2]
        return dataB

    def runBack(self, dataB):
        clusterB = self.B.run(dataB)
        clusterA = np.argmax(self.map[:,clusterB])
        if (len(self.A.w.shape) == 1 and clusterA == 0):
            dataA = self.A.w
        else:
            dataA = self.A.w[clusterA]
        return dataA
        
        
        
        
        
        
            
        
        
        
        
        
        
        
        
        
        
        

