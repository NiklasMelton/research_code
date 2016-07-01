#system test
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
screen = pygame.display.set_mode(size)
#truck dimensions
LTruck = 80
wTruck = 20
LCab = 30
wCab = 20
steer = 0

#goal position
goal = [0.0,0.5, 0.5]


#neural network setup
error = 1
count = 0
show = 0
avgError = .3

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
       if out[3] < 0:
              out[3] +=2*pi
       out[3] = out[3]/math.radians(140)
       return out

def kinematics(state, s):
       
       global width, height, pi, LTruck, LCab
       speed = -1
       cState = deNormalize(state,s)
       xTruck = cState[0]
       yTruck = cState[1]
       thetaTruck = cState[2]
       thetaCab = cState[3]
       steer = cState[4]
       print(s)
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

       if newState[3] < 0 or newState[3] > 1:
              print('------------------------------------here------------------------------')
              time.sleep(10)
       return newState



def newPosition(avgError):
       dock = [0,300]
       xmin =  5
       xmax = xmin+5 + ((1000-xmin-5)*(1-avgError))
       ymid = 300
       yrange = 295*(1-avgError)
       x = random.randrange(int(xmin), int(xmax))
       y = random.randrange(int(ymid - 5 - yrange), int(ymid + 5 + yrange))
       goalAngle = math.atan2((dock[1]-y),(dock[0]-x))
       if goalAngle < 0:
              goalAngle += 2*pi
       goalAngle = math.degrees(goalAngle)
       
       nDist = math.hypot((x-dock[0]),(y-dock[1]))/(math.hypot(1000, 300))
       ttrange = 80*(1-avgError)*(nDist)
       tt = math.radians(random.randrange(int(goalAngle - 5 - ttrange), int(goalAngle + 5 + ttrange)))
       
       if tt > 2*pi:
              tt -= 2*pi
       if tt < 0:
              tt += 2*pi
       tcrange = int(60*(1-avgError)*nDist)
       tc = math.radians(random.randrange((- 5 - tcrange), (5 + tcrange))) 
       tc += math.radians(70)
       print(x, y, tt, tc)
       state = [x/1000, y/600, tt/(2*pi), tc/(math.radians(140))]

       return state





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
       pygame.display.flip()


stateK = newPosition(avgError)

while(1):
       for event in pygame.event.get():
              if event.type == pygame.QUIT: sys. exit()
              if event .type == pygame.KEYDOWN:
                     if event.key == pygame.K_BACKSPACE:
                            stateK = newPosition(avgError)
                            print('----------------------newState', stateK)
                     if event.key == pygame.K_LEFT:
                            steer -= 0.05
                     if event.key ==pygame.K_RIGHT:
                            steer += 0.05
       stateK =  kinematics(stateK, steer)
       drawTruck(stateK)
       time.sleep(.1)
       screen.fill(white)
       
       


