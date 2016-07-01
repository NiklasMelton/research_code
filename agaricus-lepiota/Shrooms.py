#Author: Niklas Melton
#Date: 26/05/2016
#Classification of the genera agaricus and lepiota using fuzzy ARTMAP

import numpy as np, ARTMAP

rho = 0.7
alpha = 0.1
beta = 0.9

trainingNum = 6000
testShroomCount = 0
numCorrect = 0

file = open('agaricus-lepiota.data','r')
data = file.read().splitlines()

features = np.zeros(123)
numFeatKnown = 0
featureMap = np.zeros(22, dtype = object)
for i in range(0,22):
    featureMap[i] = np.array(['.',0])
edibility = np.array([])

A = ARTMAP.ARTMAP(rho, alpha, beta)
print("ART Start\n")
print("-----Learning------")
shroomCount = 0
for shroomCount in range(0,trainingNum):
    randIdx = np.random.randint(0,len(data))
    shroom = data[randIdx]
    del data[randIdx]
    #split variables
    shroom = shroom.split(',')

    #determine edibility
    if shroom[0] == 'e':
        edibility = np.array([1,0])
    else:
        edibility = np.array([0,1])

    #initialize feature array
    features = np.zeros(123)
    #for each of the 22 other variables
    for i in range(1,len(shroom)):
        #read each variable and set corersponding ART node high
        if not(featureMap[i-1] == shroom[i]).any():
            #new variable encountered
            featureMap[i-1] = np.vstack((featureMap[i-1],np.array([shroom[i],numFeatKnown])))
            features[numFeatKnown] = 1 
            numFeatKnown = numFeatKnown+1
        else:
            loc = np.where(featureMap[i-1] == shroom[i])

            map_idx = loc[0][0]
            index = featureMap[i-1][map_idx][1]
            index = int(index)
            features[index] = 1
    
    #process data sets with ARTMAP
    A.supervised(features, edibility)
    #print(3, A.map)

#------Now test identification with untrained data----------
print("-----------TEST----------\n\n")
print("Beginning testing")

for shroom in data:
    skip = False
    #print("tShroom: ",testShroomCount+1)
    #split variables
    shroom = shroom.split(',')

    #determine edibility
    if shroom[0] == 'e':
        edibility = np.array([1.0,0.0])
    else:
        edibility = np.array([0.0,1.0])

    #initialize feature array
    features = np.zeros(123)
    #for each of the 22 features
    for i in range(1,len(shroom)):
        #read each variable and set corersponding ART node high
        if not(np.any(featureMap[i-1] == shroom[i])):
            #new variable encountered
            Skip = True
            break
        else:
            loc = np.where(featureMap[i-1] == shroom[i])
            map_idx = loc[0][0]
            index = featureMap[i-1][map_idx][1]
            index = int(index)
            features[index] = 1
    if not(skip):
        #process data sets with ARTMAP
        
        prediction = A.runForward(features)
        #print(prediction, edibility)
        if (prediction == edibility).all():
            numCorrect = numCorrect + 1
        testShroomCount = testShroomCount+1

            
#print(A.map)
print("Congrats, we finally made it!\n")
print("Correct: ",numCorrect)
print("Total: ", testShroomCount)
print("Accuracy: ",numCorrect/testShroomCount)
