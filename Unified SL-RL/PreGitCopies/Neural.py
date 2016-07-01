#Nerural Network Functions
import math

def sigmoid(x):
       y = 1/(1+math.e**(-x))
       return y

def matrix(i, j, k=None):
       matrix = []
       for a in range(0, i):
              matrix.append([])
              for b in range(0, j):
                     matrix[a].append([])
                     if k !=None:
                            for c in range(0, k):
                                   matrix[b].append([])
       return matrix
                            
              
def normalize(x,xmin,xmax,r=None):
    y = (x - xmin)/(xmax-xmin)
    if r == 1:
        if y > 1:
            y = (x - xmin - (xmax-xmin))/(xmax-xmin)
        if y < 0:
            y = (x - xmin + (xmax-xmin))/(xmax-xmin)
            y = 1+y
    else:
        if y > 1:
            y = 1
            print('Over max Value for this variable')
        if y < 0:
            y = 0
            print('Below min Value for this variable')
    return y

def feedForward(X,a,b):
    #assume weights to be [j,i] vector ordering
    Y = [0]*len(a)
    Z = [0]*len(b)
    for y in range(0, len(Y)):
        for x in range(0, len(X)):
              Y[y] += a[y][x]*X[x]
        Y[y] = sigmoid(Y[y])
        
    for z in range(0, len(Z)):
        for y in range(0, len(Y)):
               Z[z] += b[z][y]*Y[y]
        Z[z] = sigmoid(Z[z])

       
       
    if len(Z) == 1:
       Z = Z[0]
    return Y, Z

def backpropogate(X,a,Y,b,dZ,update = None):
    dconst = 0.1
    if str(type(dZ)) == "<class 'float'>":
           dZ = [dZ]
    dY = [0]*len(Y)
    dX = [0]*len(X)
    da = matrix(len(Y),len(X))
    db = matrix(len(dZ),len(Y))
    for y in range(0, len(Y)):
        ySum = 0
        for z in range(0, len(dZ)):
            ySum += dZ[z]*b[z][y]
            if update == 1:
                db[z][y] = dZ[z]*Y[y]
        dY[y] = (Y[y]*(1-Y[y])+dconst)*ySum 
    for x in range(0, len(X)):
        xSum = 0
        for y in range(0, len(Y)):
            xSum += dY[y]*a[y][x]
            if update == 1:
                da[y][x] = dY[y]*X[x]
        dX[x] = (X[x]*(1-X[x])+dconst)*xSum
    
    if update == 1:
        return da, db

    else:
        return dX



def update(w,dw,LR):
    for j in range(0, len(w)):
        for i in range(0, len(w[j])):
            w[j][i] -= LR*dw[j][i]
    return w
                   
