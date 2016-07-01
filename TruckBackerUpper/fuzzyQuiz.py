#Fuzzy quiz

import sys, pygame, math, time


pygame.init()
pi = math.pi
size = width, height = 1000, 600
white = 255,255,255
black = 0, 0, 0
blue = 0,0,255
red = 255, 0, 0
green = 0,255,0
yellow = 255,255,0

screen = pygame.display.set_mode(size)
screen.fill(white)
font = pygame.font.SysFont("Comic Sans MS", 10)

#truck dimensions
LTruck = 80
wTruck = 20
LCab = 30
wCab = 20

#goal position
goal = [0.0, 0.5, 0.5, 0.5]


fuzzySteer = ['VL', 'L', 'SL', 'SR', 'R', 'VR']
fuzzyR = [0,0]
fuzzyA = [0,0,0,0]
fuzzyTT = [0,0,0,0]
fuzzyTC = [0,0,0,0]
fuzzyState = [fuzzyR, fuzzyA, fuzzyTT, fuzzyTC]

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

sets = [rSet, aSet, ttSet, tcSet]

fuzzyFile = open('fuzzyFile', 'w')

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


def drawTruck(state):
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


def midList(myList):
       n = len(myList)
       n = int((n+1)/2)
       n -= 1
       return myList[n]


while(1):
       total = len(fuzzyState[0])*len(fuzzyState[1])*len(fuzzyState[2])*len(fuzzyState[3])
       print('hello')
       time.sleep(5)
       i = 0
       for a in range(0, len(sets[0])):
              cR = midList(sets[0][a])
              for b in range(0, len(sets[1])):
                     cA= midList(sets[1][b])
                     for c in range(0, len(sets[2])):
                            cTT = midList(sets[2][c])
                            for d in range(0, len(sets[3])):
                                   pygame.event.get()
                                   i += 1
                                   cTC = midList(sets[3][d])
                                   cState = [math.cos(cA)*cR, (math.sin(cA)*cR)+0.5, cTT, cTC]
                                   drawTruck(cState)
                                   print(i, '/', total, '------',cState)
                                   yn = 'n'
                                   ask = 0
                                   while(ask == 0):
                                          while(yn != 'y'):
                                                 turn = input('How should we turn?')
                                                 yn = input('correct? (y/n)')
                                                 if yn == 'c':
                                                        screen.fill(white)
                                          if turn in fuzzySteer:
                                                 ask = 1
                                                 fuzzyFile.write(turn + '\n')
                                                 if fuzzySteer.index(turn) < 3:
                                                        color = yellow
                                                 else:
                                                        color = green
                                                 label = font.render(turn, 3, color)

                                                        
                                          else:
                                                 ask =0


                                   
       
       print('all done!')
       fuzzyFile.close()

       time.sleep(1000)
       break
                                   
