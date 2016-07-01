#Fuzzy Truck
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
goal = [0.0, 0.5, 0.5]

#fuzzy setup
aVLow = [math.radians(-90), math.radians(-54), math.radians(-18)]
aSLow = [math.radians(-54), math.radians(-18), math.radians(18)]
aSBig = [math.radians(-18), math.radians(18), math.radians(54)]
aVBig = [math.radians(18), math.radians(54), math.radians(90)]
aSet= [aVLow, aSLow, aSBig, aVBig]

rClose = [0.0, 0.2, 0.4]
rFar = [0.2, 0.4, 1]
rSet = [rClose, rFar]

ttVLow = [0.0, 0.2, 0.4]
ttLow = [0.2, 0.4, 0.6]
ttBig = [0.4, 0.6, 0.8]
ttVBig = [0.6, 0.8, 1.0]
ttSet = [ttVLow, ttLow, ttBig, ttVBig]

tcVN = [0.0, 0.2, 0.4]
tcSN = [0.2, 0.4, 0.6]
tcSP = [0.4, 0.6, 0.8]
tcVP = [0.6, 0.8, 1.0]
tcSet = [tcVN, tcSN, tcSP, tcVP]

VL = [0.0, 0.1, 0.2]
L = [0.1, 0.35, 0.45]
SL = [0.4, 0.45, 0.5]
F = [0.4, 0.5, 0.6]
SR = [0.5, 0.55, 0.6]
R = [0.55, 0.65, 0.9]
VR = [0.8, 0.9, 1.0]
steerSet = [VL, L, SL, F, SR, R, VR]


fuzzyFile = open('fuzzyFile', 'r')
fuzzyLogicDefs = list()
for i in range(0, 180):
       buffChar = fuzzyFile.readline()
       if buffChar == 'VL\n':
              fuzzyLogicDefs.append(0)
       elif buffChar == 'L\n':
              fuzzyLogicDefs.append(1)
       elif buffChar == 'SL\n':
              fuzzyLogicDefs.append(2)
       elif buffChar == 'F\n':
              fuzzyLogicDefs.append(3)
       elif buffChar == 'SR\n':
              fuzzyLogicDefs.append(4)
       elif buffChar == 'R\n':
              fuzzyLogicDefs.append(5)
       elif buffChar == 'VR\n':
              fuzzyLogicDefs.append(6)

def RectToPolar(x, y):
       r = math.hypot(x, y)
       theta = math.atan2(y, x)
       return r, theta


def fuzzify(Set, x):
       memberValues = list()
       for i in range(0, len(Set)):
              memberValues.append(0)
              
              if i == 0:
                     if x < Set[i][0]:
                            print('error, value too small')
                     elif x <= Set[i][1]:
                            memberValues[i] = 1
                     elif x < Set[i][2]:
                            memberValues[i] = 1 + (x-Set[i][1])/(Set[i][1] - Set[i][2])
                     else:
                            memberValues[i] = 0
              elif i == (len(Set)-1):
                     if x < Set[i][0]:
                            memberValues[i] = 0
                     elif x < Set[i][1]:
                            memberValues[i] = (x-Set[i][0])/(Set[i][1] - Set[i][0])
                     elif x <= Set[i][2]:
                            memberValues[i] = 1
                     else:
                            print('error, value too big', x, Set[i])
              else:
                     if x > Set[i][0] and x <= Set[i][1]:
                            memberValues[i] = (x-Set[i][0])/(Set[i][1] - Set[i][0])
                     elif x > Set[i][1] and x < Set[i][2]:
                            memberValues[i] = 1 + (x-Set[i][1])/(Set[i][1] - Set[i][2])
                     else:
                            memberValues[i] = 0
       

       return memberValues



def newPosition():
       print('goal position is:', 'x=',goal[0]*1000,'y=', goal[1]*600,'truckAngle=', goal[2]*360)
       x = float(input('Enter new x position(0-1000)'))
       y = float(input('Enter new y position(0-600)'))
       tt = float(input('Enter new truck angle(0-360'))
       tc = float(input('Enter new cab angle(0-70)'))
       x = x/1000.0
       y = y/600.0
       tt = tt/360.0
       tc = tc/70.0

       state = [x,y,tt,tc]
       return state

def fuzzifyState(state):
       fuzzyState = list(state)
       fuzzyState[0] = fuzzify(rSet, state[0])
       fuzzyState[1] = fuzzify(aSet, state[1])
       fuzzyState[2] = fuzzify(ttSet, state[2])
       fuzzyState[3] = fuzzify(tcSet, state[3])
       
       return fuzzyState

def centroid(fuzzyOut, outSet):
       outSum = 0
       totalArea = 0
       for i in range(0, len(fuzzyOut)):
              if i == 0:
                    xA = outSet[i][0]
                    xB = (1-fuzzyOut[i])*(outSet[i][2] - outSet[i][1]) + outSet[i][1]
              elif i == (len(outSet)-1):
                     xA = fuzzyOut[i]*(outSet[i][1] - outSet[i][0]) + outSet[i][0]
                     xB = outSet[i][2]
              else:
                     xA = fuzzyOut[i]*(outSet[i][1] - outSet[i][0]) + outSet[i][0]
                     xB = (1-fuzzyOut[i])*(outSet[i][2] - outSet[i][1]) + outSet[i][1]
                     
              Area =  fuzzyOut[i]*0.5*((xB-xA) + (outSet[i][2] - outSet[i][0]))
              
              outSum += fuzzyOut[i]*Area
              totalArea += Area
       
       out = outSum/totalArea

       return out
                     
                    

def fuzzyLogic(fState):
       fuzzySteer = [0, 0, 0, 0, 0, 0, 0]
       for a in range(0, len(fState[0])):
              if fState[0][a] > 0:        
                     for b in range(0, len(fState[1])):
                            if fState[1][b] > 0:
                                   for c in range(0, len(fState[2])):
                                          if fState[2][c] > 0:
                                                 for d in range(0, len(fState[3])):
                                                        if fState[3][d] > 0:
                                                               ruleIndex = int((45*a)+(15*b)+(3*c)+(d))
                                                               
                                                               steerIndex = fuzzyLogicDefs[ruleIndex]
                                                               fuzzySteer[steerIndex] += fState[0][a]*fState[1][b]*fState[2][c]*fState[3][d]
       return fuzzySteer

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
       global width, height, pi
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
       if out[3] > 0.99:
              out[3] = 0.99
       if out[2] < 0.0001:
              out[2] = 1.0
       if out[2] > 0.9999:
              out[2] = 0.0
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
       #print(newState)

       return newState


def drawTruck(state):
       screen.fill(white)
       pygame.event.get()
       cState = deNormalize(state,0.5)
       xTruck = cState[0]
       yTruck = cState[1]
       thetaTruck = cState[2]
       thetaCab = cState[3]
       xCab = xTruck - LTruck*math.cos(-thetaTruck)
       yCab = yTruck - LTruck*math.sin(thetaTruck)
       xWheel = xCab + LCab*math.cos(thetaCab)
       yWheel = yCab + LCab*math.sin(thetaCab)
       pygame.draw.polygon(screen, red, [(xCab,yCab),(xCab+14*math.cos(0.785398+thetaCab),yCab+14*math.sin(0.785398+thetaCab)), (xWheel-10*math.sin(thetaCab), yWheel+10*math.cos(thetaCab)), (xWheel +10*math.sin(thetaCab), yWheel-10*math.cos(thetaCab)), (xCab+14*math.cos(thetaCab-0.785399), yCab+14*math.sin(thetaCab-0.78539))], 2)
       pygame.draw.polygon(screen, red, [(xTruck+10*math.sin(-thetaTruck),yTruck+10*math.cos(thetaTruck)),(xCab+10*math.sin(-thetaTruck),yCab+10*math.cos(thetaTruck)),(xCab-10*math.sin(-thetaTruck),yCab-10*math.cos(thetaTruck)),(xTruck-10*math.sin(-thetaTruck),yTruck-10*math.cos(thetaTruck))], 2)
       pygame.draw.circle(screen, green, (0, 300), 10)
       pygame.display.flip()



       
while(1):
       
       stateK = newPosition()
       
       while(stateK[0] > 0):
              drawTruck(stateK)
              print('check')
              pstateK = list(stateK)
              polarPos = RectToPolar(stateK[0], stateK[1]-0.5)
              pstateK[0] = polarPos[0]
              pstateK[1] = polarPos[1]
              pstateK[2] = stateK[2]
              pstateK[3] = stateK[3]
              print(pstateK)
              fuzzyStateK = fuzzifyState(pstateK)
              print(fuzzyStateK)
              fuzzySteer = fuzzyLogic(fuzzyStateK)
              print(fuzzySteer)
              steer = centroid(fuzzySteer, steerSet)
              newState = kinematics(stateK, steer)
              stateK = newState
              
              

       
       

       

       
