#emulator Driver
#truck controller
import sys, pygame
import sys, math
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

EalphaWeight = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
EbetaWeight = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 

eFile = open('EmulatorFile', 'r')
for a in range(0, len(EalphaWeight)):
       EalphaWeight[a] = float(eFile.readline())
for b in range(0, len(EbetaWeight)):
       EbetaWeight[b] = float(eFile.readline())
eFile.close()

def sigmoid(x):
       y = 1/(1+math.e**(-x))
       return y

def emulator(inx,s):
       #5 input, 25 hidden, 4 output
       inputNode = inx
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



       return outputNode

def drawTruck(state):
       xCab = state[0]*width
       yCab = state[1]*height
       thetaTruck = state[2]*2*pi
       thetaCab = state[3]*math.radians(140) - pi + thetaTruck
       xTruck = xCab + LTruck*math.cos(-thetaTruck)
       yTruck = yCab + LTruck*math.sin(thetaTruck)
       xWheel = xCab + LCab*math.cos(thetaCab)
       yWheel = yCab + LCab*math.sin(thetaCab)
       pygame.draw.polygon(screen, red, [(xCab,yCab),(xCab+14*math.cos(0.785398+thetaCab),yCab+14*math.sin(0.785398+thetaCab)), (xWheel-10*math.sin(thetaCab), yWheel+10*math.cos(thetaCab)), (xWheel +10*math.sin(thetaCab), yWheel-10*math.cos(thetaCab)), (xCab+14*math.cos(thetaCab-0.785399), yCab+14*math.sin(thetaCab-0.78539))], 2)
       pygame.draw.polygon(screen, red, [(xTruck+10*math.sin(-thetaTruck),yTruck+10*math.cos(-thetaTruck)),(xCab+10*math.sin(-thetaTruck),yCab+10*math.cos(-thetaTruck)),(xCab-10*math.sin(-thetaTruck),yCab-10*math.cos(-thetaTruck)),(xTruck-10*math.sin(-thetaTruck),yTruck-10*math.cos(-thetaTruck))], 2)
       pygame.display.flip()



go = 0
while(1):
       for event in pygame.event.get():
                     if event.type == pygame.QUIT: sys. exit()
                     if event .type == pygame.KEYDOWN:
                            if event.key == pygame.K_BACKSPACE:
                                   go = 1
                                   #initial position
                                   screen.fill(white)
                                   xTruck = 850/width
                                   yTruck = 300/height
                                   thetaTruck = pi/(2*pi)
                                   thetaCab = 0/math.radians(140)
                                   steer = 0
                                   StateK = [xTruck, yTruck, thetaTruck, thetaCab]
                     
       while(go == 1):

       
              for event in pygame.event.get():
                     if event.type == pygame.QUIT: sys. exit()
                     if event .type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT and steer > -20:
                                   steer -= 1
                            if event.key == pygame.K_RIGHT and steer < 20:
                                   steer += 1
                            if event.key == pygame.K_BACKSPACE:
                                   go = 0
              if StateK[0] < 0:
                     go = 0
                     

              nsteer = math.radians(steer+20)/math.radians(40)
              StateK = emulator(StateK, nsteer)
              drawTruck(StateK)
              time.sleep(0.3)
              
