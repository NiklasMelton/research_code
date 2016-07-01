#truck emulator

import sys, math
import sys, random
import sys, time


pi = math.pi
size = width, height = 1000, 600
#truck dimensions
LTruck = 80
wTruck = 20
LCab = 30
wCab = 20



def sigmoid(x):
       y = 1/(1+math.e**(-x))
       return y

def RectToPolar(x, y):
       nx = x*width
       ny = (y-0.5)*height
       theta = math.atan2(ny,nx)
       r = math.hypot(nx, ny)
       ntheta = (theta+(pi/2))/(pi)
       nr = r/(math.hypot(width, 0.5*height))
       return ntheta, nr



#neural network setup
error = 1
avgError = 1
learningRate = 0.4
#5 input, 25 hidden, 4 output
inputNode = [0, 0, 0, 0, 0]
hiddenNode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
outputNode = [0, 0, 0, 0]
alphaWeight = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
betaWeight = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
#initialize weights randomly
for w in range(0,125):
       alphaWeight[w] = random.random()
for w in range(0,100):
       betaWeight[w] = random.random()

count = 0
while(avgError > 0.002):
 


       #initial position
       xTruck = random.randrange(5, width-5)     #between 5 and width-5
       nxTruck = xTruck/width
       yTruck = random.randrange(0, height - 5)       #between 0 and height-5
       nyTruck = yTruck/height
       thetaTruck = math.radians(random.randrange(0,360))      #between 0 and 2pi
       nthetaTruck = thetaTruck/(2*pi)
       thetaCab = math.radians(random.randrange(-70, 70))     #between -70 and 70
       nthetaCab = round((thetaCab+ math.radians(70))/math.radians(140), 2)
       thetaCab = thetaTruck - pi + thetaCab
       xCab = xTruck - LTruck*math.cos(thetaTruck)      
       yCab = yTruck + LTruck*math.sin(-thetaTruck)
       steer = math.radians(random.randrange(0,40))     #between 0 and 40
       nsteer = steer/math.radians(40)
       steer -= math.radians(20)
       speed = -1
       
       

       #fill and normalize input layer (NN)
       polar = RectToPolar(nxTruck, nyTruck)
       inputNode[0] = polar[0]
       inputNode[1] = polar[1]
       inputNode[2] = nthetaTruck
       inputNode[3] = nthetaCab
       inputNode[4] = nsteer
       

       
       #compute hidden layer (NN)
       hiddenNode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
       for h in range(0,len(hiddenNode)):
              for i in range(0, len(inputNode)):
                     hiddenNode[h] = hiddenNode[h] + inputNode[i]*alphaWeight[(i + h*len(inputNode))]
              hiddenNode[h] = sigmoid(hiddenNode[h])
              

       #compute output layer (NN)
       outputNode = [0, 0, 0, 0]
       for o in range(0, len(outputNode)):
              for h in range(0, len(hiddenNode)):
                     outputNode[o] = outputNode[o] + hiddenNode[h]*betaWeight[(h + o*len(hiddenNode))]
              outputNode[o]  = sigmoid(outputNode[o])

       #kinematics
       thetaCab += speed*math.tan(steer)/LCab
       xCab = xCab + speed*math.cos(-thetaCab)
       yCab = yCab + speed *math.sin(thetaCab)
       thetaTruck = thetaTruck + speed*math.sin(thetaTruck - thetaCab)/LTruck
       xTruck = xCab + LTruck*math.cos(-thetaTruck)
       yTruck = yCab + LTruck*math.sin(thetaTruck)
       
       nthetaCab = (thetaCab - thetaTruck + pi)
       if abs(nthetaCab) > 2*pi:
              nthetaCab -= 2*pi*nthetaCab/abs(nthetaCab)

       nxTruck = xTruck/width
       nyTruck = yTruck/height
       polarK = RectToPolar(nxTruck, nyTruck)
       nthetaCab = round((nthetaCab + math.radians(70))/(math.radians(140)),2)
       nthetaTruck = round(thetaTruck/(2*pi), 3)
       

       
       #Back-Propogation
       outDelta = [0, 0, 0, 0]

       outDelta[0] = outputNode[0]*(1-outputNode[0])*(outputNode[0]-polarK[0])
       outDelta[1] = outputNode[1]*(1-outputNode[1])*(outputNode[1]-polarK[1])
       outDelta[2] = outputNode[2]*(1-outputNode[2])*(outputNode[2]-nthetaTruck)
       outDelta[3] = outputNode[3]*(1-outputNode[3])*(outputNode[3]-nthetaCab)

       hiddenDelta = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
       for h in range(0, len(hiddenDelta)):
              hiddenSum = 0
              for o in range(0, len(outDelta)):
                     hiddenSum = hiddenSum + outDelta[o]*betaWeight[(h+o*len(outDelta))]
              hiddenDelta[h] = hiddenNode[h]*(1-hiddenNode[h])*hiddenSum



       for o in range(0, len(outputNode)):
              for h in range(0, len(hiddenNode)):
                     betaWeight[(h + o*len(hiddenNode))] = betaWeight[(h+ o*len(hiddenNode))] - learningRate*outDelta[o]*hiddenNode[h]

       for h in range(0, len(hiddenNode)):
              for i in range(0, len(inputNode)):
                     alphaWeight[(i + h*len(inputNode))] = alphaWeight[(i + h*len(inputNode))] - learningRate*hiddenDelta[h]*inputNode[i]

                     
       error = 0.5*((outputNode[0] - nxTruck)**2 + (outputNode[1] - nyTruck)**2 + (outputNode[2] - nthetaTruck)**2  + (outputNode[3] - nthetaCab)**2) 
       avgError = (avgError*300 + error)/301
       print(error, '       - ', avgError, '       - ', count)
       if error > math.sqrt(avgError):
              print('out',str(nxTruck), str(nyTruck), str(nthetaTruck), str(nthetaCab))
              print(polar, polarK)
       count += 1
       if abs(nxTruck) >1 or abs(nyTruck) > 1 or abs(nthetaTruck) > 1 or abs(nthetaCab) > 1:
              print('out',str(nxTruck), str(nyTruck), str(nthetaTruck), str(nthetaCab))
              break


       
File = open('EmulatorFile', 'w')
for a in range(0, len(alphaWeight)):
       File.write(str(alphaWeight[a])+'\n')
for b in range(0, len(betaWeight)):
       File.write(str(betaWeight[b])+'\n')
File.write('x\n' + str(error) + '\n')
File.close()
       






       
