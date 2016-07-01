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

eFile = open('EmulatorFile', 'r')
for a in range(0, len(EalphaWeight)):
       EalphaWeight[a] = float(eFile.readline())
for b in range(0, len(EbetaWeight)):
       EbetaWeight[b] = float(eFile.readline())
eFile.close()

yn = input('start from scratch?')
if yn == 'y':
       #initialize weights randomly
       for w in range(0,100):
              CalphaWeight[w] = random.uniform(-1.0,1.0)
       for w in range(0,25):
              CbetaWeight[w] = random.uniform(-1.0,1.0)
else:
       cFile = open('ControllerFile', 'r')
       for a in range(0, len(CalphaWeight)):
              CalphaWeight[a] = float(cFile.readline())
       for b in range(0, len(CbetaWeight)):
              CbetaWeight[b] = float(cFile.readline())
       cFile.close()


def sigmoid(x):
       y = 1 / (1+math.exp(-x))
       return y

def emulator(inx,s):
       
       #5 input, 25 hidden, 4 output
       inputNode = list(inx)
       inputNode.append(s)
       hiddenNode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
       outputNode = [0, 0, 0, 0]
       global EalphaWeight
       global EbetaWeight

        #compute hidden layer (NN)
       for h in range(0,len(hiddenNode)):
              for i in range(0, len(inputNode)):
                     hiddenNode[h] = hiddenNode[h] + inputNode[i]*EalphaWeight[(i+h*len(inputNode))]
              hiddenNode[h] = sigmoid(hiddenNode[h])
              

       #compute output layer (NN)
       for o in range(0, len(outputNode)):
              for h in range(0, len(hiddenNode)):
                     outputNode[o] = outputNode[o] + hiddenNode[h]*EbetaWeight[(h + o*len(hiddenNode))]
              outputNode[o]  = sigmoid(outputNode[o])


       for h in range(0, len(hiddenNode)):
              EhmemVar.append(hiddenNode[h])
              
       for o in range(0, len(outputNode)):
              EomemVar.append(outputNode[o])

       

       
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
       

       for i in range(0, 4):
              CimemVar.append(inputNode[i])
       for h in range(0, 25):
              ChmemVar.append(hiddenNode[h])
              

       ComemVar.append(outputNode[0])
       
       return outputNode[0]


       
def error(state, goal):
       error = .5*((state[0] - goal[0])**2 + (state[1] - goal[1])**2 + (state[2] - goal[2])**2)
       return error


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
       
       global width, height, pi, LTruck, LCab, jk, stateJK, hold
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



def newPosition():
       global expander, avgError, stepMax, CalphaWeight, CbetaWeight, xmax, yrange, ttrange, tcrange
       if avgError < 0.03:
              print('prev xmax = ', xmax, '0-1000')
              xmax = int(input('xmax == '))
              print('prev yrange = ', yrange, '0-300')
              yrange  = int(input('yrange == '))
              print('prev ttrange = ', ttrange, '0-180')
              ttrange = int(input('ttrange == '))
              print('prev tcrange = ', tcrange, '0-70')
              tcrange = int(input('tcrange == '))
              avgError = 1
              File = open('ControllerFile', 'w')
              for a in range(0, len(CalphaWeight)):
                     File.write(str(CalphaWeight[a])+'\n')
              for b in range(0, len(CbetaWeight)):
                     File.write(str(CbetaWeight[b])+'\n')
              File.close()
              
       dock = [0,300]
       x = random.randrange(300, xmax)
       y = random.randrange(300 - yrange, 300+yrange)
       stepMax = 1.2*math.hypot(x, y)
       goalAngle = math.atan2((dock[1]-y),(dock[0]-x))
       if goalAngle < 0:
              goalAngle += 2*pi
       goalAngle = math.degrees(goalAngle)
       
       #nDist = math.hypot((x-dock[0]),(y-dock[1]))/(math.hypot(1000, 300))
       
       tt = math.radians(random.randrange(int(goalAngle-ttrange), int(goalAngle+ttrange)))
       
       if tt > 2*pi:
              tt -= 2*pi
       if tt < 0:
              tt += 2*pi
       
       tc = math.radians(random.randrange(-tcrange, tcrange)) 
       tc += math.radians(70)
       state = [x/1000, y/600, tt/(2*pi), tc/(math.radians(140))]

       return state





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
       pygame.draw.polygon(screen, red, [(xCab,yCab),(xCab+14*math.cos(0.785398+thetaCab),yCab+14*math.sin(0.785398+thetaCab)), (xWheel-10*math.sin(thetaCab), yWheel+10*math.cos(thetaCab)), (xWheel +10*math.sin(thetaCab), yWheel-10*math.cos(thetaCab)), (xCab+14*math.cos(thetaCab-0.785399), yCab+14*math.sin(thetaCab-0.78539))], 2)
       pygame.draw.polygon(screen, red, [(xTruck+10*math.sin(-thetaTruck),yTruck+10*math.cos(thetaTruck)),(xCab+10*math.sin(-thetaTruck),yCab+10*math.cos(thetaTruck)),(xCab-10*math.sin(-thetaTruck),yCab-10*math.cos(thetaTruck)),(xTruck-10*math.sin(-thetaTruck),yTruck-10*math.cos(thetaTruck))], 2)
       pygame.draw.circle(screen, green, (0, 300), 10)
       pygame.display.flip()


xmax = int(input('xmax == '))
yrange  = int(input('yrange == '))
ttrange = int(input('ttrange == '))
tcrange = int(input('tcrange == '))
stateK = newPosition()
lastNew = stateK
jkCount = 0
#////////////////////////////////////////////////////////MAIN//LOOP////////////////////////////////////////////////////////////////////
while(1):

       LearningRate = .5*avgError
       if jk == 1 or error(stateK, goal) > 1.2*avgError:
              stateK = lastNew
              jkCount += 1

              if jkCount > 2 or steps >= stepMax:
                     stateK = newPosition()
                     print(stateK)
                     lastNew = stateK
                     screen.fill(white)
                     jkCount = 0
       else:
              stateK = newPosition()
              print(stateK)
              lastNew = stateK
              screen.fill(white)
              jkCount = 0

              
       count += 1
       EhmemVar = list()
       EomemVar = list()
       CimemVar = list()
       ChmemVar = list()
       ComemVar = list()
       steps = 0
       jk = 0
       
       
       while(stateK[0] > 0 and steps  < stepMax and jk == 0):
              #feedforward
              steerK = controller(stateK)
              emulator(stateK, steerK)
              newstateK = kinematics(stateK, steerK)
              stateK = newstateK
              
              steps += 1

              for event in pygame.event.get():
                     if event.type == pygame.QUIT: sys. exit()
                     if event .type == pygame.KEYDOWN:
                            if event.key == pygame.K_DOWN:
                                   show = 0
                            if event.key == pygame.K_UP:
                                   show = 1
                            if event.key == pygame.K_LEFT:
                                   hold = 1
                            if event.key == pygame.K_RIGHT:
                                   hold = 0
              if hold == 0:
                            screen.fill(white)
              if show == 1:
                     drawTruck(stateK)

                            
                     
                     
       
       if jk == 0:                     
              avgError = (avgError*filterVar + error(stateK, goal))/(filterVar+1)
       
       
       #backpropogate
       DeltaWeight = list()
       for i in range(0, (len(CalphaWeight) + len(CbetaWeight))):
              DeltaWeight.append(0)
       
       #calculate first deltas
       outputDelta = [0, 0, 0, 0]
       EhmemVar.reverse()
       EomemVar.reverse()
       CimemVar.reverse()
       ChmemVar.reverse()
       ComemVar.reverse()
       for o in range(0,4):
              outputDelta[o] = stateK[o]*(1-stateK[o])*(stateK[o] - goal[o])
       #if jk == 1:
              #print('jk----', steerK)
              #outputDelta[3] = stateK[3]*(1-stateK[3])*(stateK[3] - goal[3])
       #else:
              #outputDelta.pop(3)
       
       prevDelta = list(outputDelta)
       

       

       T = len(ComemVar)
       T = int(T)
       #repeat for all time T
       for t in range(0, T):
              Tbias = math.exp(-t/T)
              
              #fill variables:
              hiddenNode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
              CinputNode = [0,0,0,0]
              ChiddenNode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
              #Emulator hidden layer
              for h in range(0, 25):
                     hiddenNode[h] = EhmemVar[0]
                     EhmemVar.pop(0)
              hiddenNode.reverse()
              #controller hidden layer
              for h in range(0, 25):
                     ChiddenNode[h] = ChmemVar[0]
                     ChmemVar.pop(0)
              ChiddenNode.reverse()
              #controller input layer (kinematics out)
              for i in range(0, 4):
                     CinputNode[i] = CimemVar[0]
                     CimemVar.pop(0)
              CinputNode.reverse()
              #controller out
              sNode = ComemVar[0]
              ComemVar.pop(0)
              
                     
              #--------THROUGH EMULATOR       
              
              hiddenDelta = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
              for h in range(0, 25):
                     hiddenSum = 0
                     for k in range(0, len(prevDelta)):
                            hiddenSum += prevDelta[k]*EbetaWeight[(h + k*25)]
                     hiddenDelta[h] = hiddenNode[h]*(1-hiddenNode[h])*hiddenSum
       
              
              
              sSum = 0
              for k in range(0, 25):
                     sSum += hiddenDelta[k]*EalphaWeight[(4 + 5*k)]
              if sNode > 0.995:
                     sNode = 0.995
              sDelta = sNode*(1-sNode)*sSum
              if jk == 1:
                     if stateK[3] == 0.99:
                            sDelta = -abs(sDelta)
                     else:
                            sDelta = abs(sDelta)

                            
              
              
              
              #-------LEARN CONTROLLER
              
              ChiddenDelta = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
              for h in range(0, 25):
                     ChiddenSum = sDelta*CbetaWeight[h]
                     ChiddenDelta[h] = ChiddenNode[h]*(1-ChiddenNode[h])*ChiddenSum
              
              CinputDelta = [0,0,0,0]
              for i in range(0, 4):
                     CinSum = 0
                     for h in range(0, 25):
                            CinSum += ChiddenDelta[h]*CalphaWeight[(i + h*4)]
                            #CinSum += hiddenDelta[h]*EalphaWeight[(i + h*5)]
                     CinputDelta[i] = CinputNode[i]*(1-CinputNode[i])*CinSum
              

              #calculate weight deltas
              for h in range(0, 25):
                     for i in range(0, 4):   
                            DeltaWeight[(i+h*4)] -= Tbias*LearningRate*ChiddenDelta[h]*CinputNode[i]
              
              for i in range(0, len(ChiddenNode)):
                     DeltaWeight[(100+i)] -= Tbias*LearningRate*sDelta*ChiddenNode[i]
         
       #update weights
       for a in range(0, len(CalphaWeight)):
              CalphaWeight[a] += DeltaWeight[a]
       for b in range(0, len(CbetaWeight)):
              CbetaWeight[b] += DeltaWeight[(100 + b)]
                                       
       prevDelta = list(CinputDelta)
              
       if jk == 1:
              change = round(abs(steerK - oldsteer), 5)
              print('err',avgError, T, count, 'cab', stateK[3], 'steer', round(steerK,4), 'change-', change, jkCount)
              oldsteer = steerK
              
              
       else:
              print(avgError,count, steps, stepMax)
              jkCount = 0
       
                                                          
File = open('ControllerFile', 'w')
for a in range(0, len(CalphaWeight)):
       File.write(str(CalphaWeight[a])+'\n')
for b in range(0, len(CbetaWeight)):
       File.write(str(CbetaWeight[b])+'\n')
File.close()

       
       
