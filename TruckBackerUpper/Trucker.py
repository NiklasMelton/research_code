#truck controller
import sys, pygame
import sys, math
import sys, random
import sys, time

pygame.init()
pi = math.pi
size = width, height = 1000, 600
white = 255,255,255
black = 0, 0, 0
blue = 0,0,255
red = 255, 0, 0
green = 0,255,0
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont("Comic Sans MS", 10)
#truck dimensions
LTruck = 80
wTruck = 20
LCab = 30
wCab = 20

#goal position
goal = [0.0, 0.5, 0.5, 0.5]

xmax = 0
yrange = 0
ttrange = 0
tcrange = 0

#control variables
jk = 0
show = 0
hold = 0

#neural network setup
error = 1
oldsteer = 0
filterVar = 500
count = 0
avgError = 1
stepMax = 500
change = 1.0
LearningRate = 0.08
EalphaWeight = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
EbetaWeight = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
CalphaWeight = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
CbetaWeight = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

cFile = open('ControllerFile', 'r')
for a in range(0, len(CalphaWeight)):
      CalphaWeight[a] = float(cFile.readline())
for b in range(0, len(CbetaWeight)):
      CbetaWeight[b] = float(cFile.readline())
cFile.close()
       
def sigmoid(x):
       y = 1 / (1+math.exp(-x))
       return y

def controller(inx):
       inputNode = list(inx)
       hiddenNode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
       outputNode = [0]
       global CalphaWeight
       global CbetaWeight
       #compute hidden layer (NN)
       for h in range(0, 25):
              for i in range(0, 4):
                     hiddenNode[h] += inputNode[i]*CalphaWeight[(i + h*4)]
                     
              hiddenNode[h] = sigmoid(hiddenNode[h])
              
       

       #compute output layer (NN)
       for h in range(0, 25):
              outputNode[0] = outputNode[0] + hiddenNode[h]*CbetaWeight[h]
       outputNode[0]  = sigmoid(outputNode[0])
       

       
       return outputNode[0]

def deNormalize(state, s):
       #outputs xTruck between 0 and 1000
       #outputs yTruck between 0 and 600
       #outputs thetaTruck between 0 and 2*pi
       #outputs thetaCab between 0 and 2*pi
       global width, height, pi
       out = [0, 0, 0, 0, 0]
       out[0] = state[0]*width
       out[1]= state[1]*height
       out[2] = state[2]*2*pi
       out[3] =  (state[3]*math.radians(140)) - math.radians(70)
       out[3] = out[3] + out[2] + pi
       if out[3] < 0:
              out[3] += 2*pi
       if out[3] > 2*pi:
              out[3] -= 2*pi

       out[4] = s*math.radians(40) - math.radians(20)
       return out

def Normalize(state):
       #returns all between 0 and 1
       global width, height, pi, jk
       out = [0, 0, 0, 0]
       out[0] = state[0]/width
       out[1] = state[1]/height
       out[2] = state[2]/(2*pi)
       out[3] = state[3] - state[2] - pi

       out[3] += math.radians(70)

       if out[3] < -pi:
              out[3] += 2*pi
       
       out[3] = out[3]/math.radians(140)
       if out[3] < 0.01:
              out[3] = 0.01
              jk = 1
       elif out[3] > 0.99:
              out[3] = 0.99
              jk= 1
       else:
              jk = 0
              
       return out

def kinematics(state, s):
       
       global width, height, LTruck, LCab
       speed = -1
       cState = deNormalize(state,s)
       xTruck = cState[0]
       yTruck = cState[1]
       thetaTruck = cState[2]
       thetaCab = cState[3]
       steer = cState[4]
       xCab = xTruck - LTruck*math.cos(-thetaTruck)
       yCab = yTruck - LTruck*math.sin(thetaTruck)
       
       thetaCab += (speed*math.tan(steer)/LCab)
       xCab += (speed*math.cos(-thetaCab))
       yCab +=  (speed *math.sin(thetaCab))
       thetaTruck +=  (speed*math.sin(thetaTruck-thetaCab)/LTruck)
       xTruck = xCab + LTruck*math.cos(-thetaTruck)
       yTruck =  yCab + LTruck*math.sin(thetaTruck)
       newState = [xTruck, yTruck, thetaTruck, thetaCab]
       
       newState = Normalize(newState)

       return newState







def drawTruck(state):
       cState = deNormalize(state,0.5)
       xTruck = cState[0]
       yTruck = cState[1]
       thetaTruck = cState[2]
       thetaCab = cState[3]
       pstate = font.render(str(round(state[3],4)), 1, blue)
       screen.blit(pstate,((xTruck - 5),(yTruck+5)))
       xCab = xTruck - LTruck*math.cos(-thetaTruck)
       yCab = yTruck - LTruck*math.sin(thetaTruck)
       xWheel = xCab + LCab*math.cos(thetaCab)
       yWheel = yCab + LCab*math.sin(thetaCab)
       screen.fill(white)
       pygame.draw.polygon(screen, red, [(xCab,yCab),(xCab+14*math.cos(0.785398+thetaCab),yCab+14*math.sin(0.785398+thetaCab)), (xWheel-10*math.sin(thetaCab), yWheel+10*math.cos(thetaCab)), (xWheel +10*math.sin(thetaCab), yWheel-10*math.cos(thetaCab)), (xCab+14*math.cos(thetaCab-0.785399), yCab+14*math.sin(thetaCab-0.78539))], 2)
       pygame.draw.polygon(screen, red, [(xTruck+10*math.sin(-thetaTruck),yTruck+10*math.cos(thetaTruck)),(xCab+10*math.sin(-thetaTruck),yCab+10*math.cos(thetaTruck)),(xCab-10*math.sin(-thetaTruck),yCab-10*math.cos(thetaTruck)),(xTruck-10*math.sin(-thetaTruck),yTruck-10*math.cos(thetaTruck))], 2)
       pygame.draw.circle(screen, green, (0, 300), 10)
       pygame.display.flip()



#////////////////////////////////////////////////////////MAIN//LOOP////////////////////////////////////////////////////////////////////
while(1):
    x = int(input('x == '))
    y  = int(input('y == '))
    tt = math.radians(int(input('tt == ')))
    tc = math.radians(int(input('tc == '))) + tt + pi
    stateK = [x,y,tt,tc]
    stateK = Normalize(stateK)
    lastNew = stateK
    jk = 0
    steps = 0

    while(stateK[0] > 0 and steps < 700):
        steps +=1
        pygame.event.get()
        drawTruck(stateK)
        steer = controller(stateK)
        print(steer)
        stateK = kinematics(stateK, steer)
        time.sleep(0.02)
