#Author: Niklas Melton
#Date: 09/02/2016
#FuzzyART implemention.

import numpy as np

def norm(x):
#determine input norm
    normX = 0
    for i in range(0,len(x)):
        normX += abs(x[i])
    return float(normX)


def fuzzyAnd(x, y):
    return np.minimum(x,y)

class ARTnet:
    def __init__(self, rho, alpha, beta, weights=None):
        self.rho = rho
        self.alpha = alpha
        self.beta = beta
        self.w = weights
        self.clustNum = 0

    def learnRun(self, data, getCluster = True):
        inputVector = np.concatenate((data, 1-data))
        if self.w is None:
            self.w = np.array([inputVector])
            self.clustNum = 1
        else:
            self.clustNum = len(self.w)
        #determine input norm and match criterion
        normInput = norm(inputVector)
        MC = normInput*self.rho
        #Choose a category node
        T = np.zeros(self.clustNum)
        for j in range(0, self.clustNum):
            T[j] = norm(fuzzyAnd(inputVector,self.w[j]))/(self.alpha+norm(self.w[j]))
        #test each category node selected until the vigilance criteria is met
        hyp = 0
        while (hyp < MC):
            Twin = np.argmax(T)
            hyp = norm(fuzzyAnd(inputVector, self.w[Twin]))
            if hyp < MC:
                T[Twin] = 0
            if norm(T) == 0:
                #new category node needs to be created
                self.w = np.vstack([self.w, inputVector])
                self.clustNum = len(self.w)
                #forces new node selection
                Twin = len(T)
                T = np.append(T, 1)
            
                
        #update weights
        self.w[Twin] = self.beta*fuzzyAnd(inputVector, self.w[Twin]) + (1-self.beta)*self.w[Twin]   
        if getCluster == True:
            #output which node won
            return Twin

    def run(self, data, optNum = 1):
        #Identifies Cluster for data with ability to return sub optimal guesses
        #example: setting optNum = 2 returns second best guess
        inputVector = np.concatenate((data, 1-data))
        if self.w is None:
            self.w = np.array(inputVector)
            self.clustNum = 1
        else:
            self.clustNum = len(self.w)
        #determine input norm and match criterion
        normInput = norm(inputVector)
        MC = normInput*self.rho
        #Choose a category node
        T = np.zeros(self.clustNum)
        for j in range(0, self.clustNum):
            T[j] = norm(fuzzyAnd(inputVector,self.w[j]))/(self.alpha+norm(self.w[j]))
        #find best match and set to zero to find optNum'th best guess 
        for i in range(0, (optNum-1)):
            Twin = np.argmax(T)
            T[Twin] = 0
        #reevaluate to find next best guess
        Twin = np.argmax(T)
                
        #output second best guess
        return Twin

        
