#truck driver

import sys, pygame
import sys, math
import sys, time
pygame.init()
pi = math.pi
def sigmoid(x):
       y = 1/(1+math.e**(-x))
       return y

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
#initial position
xTruck = 850
yTruck = 300
thetaTruck = pi
thetaCab = 0
xCab = xTruck + LTruck
yCab = 300
steer = 0
speed = 0
#5 input, 25 hidden, 4 output
inputNode = [0, 0, 0, 0, 0]
hiddenNode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
outputNode = [0, 0, 0, 0]
alphaWeight = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
betaWeight = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
File = open('EmulatorFile', 'r')
for a in range(0, len(alphaWeight)):
       alphaWeight[a] = float(File.readline())
for b in range(0, len(betaWeight)):
       betaWeight[b] = float(File.readline())
File.close()
bigfont = pygame.font.SysFont("Comic Sans MS", 20)
littlefont = pygame.font.SysFont("Comic Sans MS", 10)


go = 1
while(1):
       for event in pygame.event.get():
                     if event.type == pygame.QUIT: sys. exit()
                     if event .type == pygame.KEYDOWN:
                            if event.key == pygame.K_BACKSPACE:
                                   go = 1
                                   #initial position
                                   xTruck = 850
                                   yTruck = 300
                                   thetaTruck = pi
                                   thetaCab = 0
                                   xCab = xTruck + LTruck
                                   yCab = 300
                                   steer = 0
                                   speed = 0
                     
       while(go == 1):

       
              for event in pygame.event.get():
                     if event.type == pygame.QUIT: sys. exit()
                     if event .type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT and steer > -19:
                                   steer -= 1
                            if event.key == pygame.K_RIGHT and steer < 19:
                                   steer += 1
                            if event.key == pygame.K_BACKSPACE:
                                   go = 0

              steer = math.radians(steer)
              speed = -1
              
              
              
              #fill and normalize input layer (NN)
              inputNode[0] = xTruck/width
              inputNode[1] = yTruck/height
              inputNode[2] = thetaTruck/(2*pi)
              while(abs(inputNode[2]) > 1):
                     inputNode[2] -= inputNode[2]/abs(inputNode[2])
              nthetaCab = thetaCab - thetaTruck + math.pi
              if abs(nthetaCab) > 2*pi:
                     nthetaCab -= 2*pi*nthetaCab/abs(nthetaCab)
              inputNode[3] = (nthetaCab + math.radians(70))/(math.radians(140))
              while(abs(inputNode[3]) > 1):
                     inputNode[3] -= inputNode[3]/abs(inputNode[3])
              inputNode[4] = (steer + math.radians(20))/(math.radians(40))

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
              xWheel = xCab + LCab*math.cos(thetaCab)
              yWheel = yCab + LCab*math.sin(thetaCab)



              nthetaCab = (thetaCab - thetaTruck + pi)
              if abs(nthetaCab) > 2*pi:
                     nthetaCab -= 2*pi*nthetaCab/abs(nthetaCab)

              nxTruck = xTruck/width
              nyTruck = yTruck/height
              nthetaCab = round((nthetaCab + math.radians(70))/(math.radians(140)),2)
              nthetaTruck = round(thetaTruck/(2*pi), 3)

              error = 0.5*((outputNode[0] - nxTruck)**2 + (outputNode[1] - nyTruck)**2 + (outputNode[2] - nthetaTruck)**2  + (outputNode[3] - nthetaCab)**2) 
              Error = bigfont.render(str(error), 1, blue)
              kx = littlefont.render(str(round(nxTruck,2)), 1, blue)
              ky = littlefont.render(str(round(nyTruck,2)), 1, blue)
              ktt = littlefont.render(str(round(nthetaTruck,2)), 1, blue)
              ktc = littlefont.render(str(round(nthetaCab,2)), 1, blue)
              #draw truck then turn indicator
              screen.fill(white)
              #pygame.draw.lines(screen, black, False, [(xTruck,yTruck),(xCab,yCab),(xWheel,yWheel)], 5)
              pygame.draw.polygon(screen, red, [(xCab,yCab),(xCab+14*math.cos(0.785398+thetaCab),yCab+14*math.sin(0.785398+thetaCab)), (xWheel-10*math.sin(thetaCab), yWheel+10*math.cos(thetaCab)), (xWheel +10*math.sin(thetaCab), yWheel-10*math.cos(thetaCab)), (xCab+14*math.cos(thetaCab-0.785399), yCab+14*math.sin(thetaCab-0.78539))])
              pygame.draw.polygon(screen, red, [(xTruck+10*math.sin(-thetaTruck),yTruck+10*math.cos(-thetaTruck)),(xCab+10*math.sin(-thetaTruck),yCab+10*math.cos(-thetaTruck)),(xCab-10*math.sin(-thetaTruck),yCab-10*math.cos(-thetaTruck)),(xTruck-10*math.sin(-thetaTruck),yTruck-10*math.cos(-thetaTruck))])
              pygame.draw.rect(screen, red, (450, 40, 90, 20))
              steer = int(math.degrees(steer))
              pygame.draw.circle(screen,blue,(int(495+steer), 50), 15)
              screen. blit(Error, (800,30))
              screen.blit(kx, (800, 550))
              screen.blit(ky, (850, 550))
              screen.blit(ktt, (900, 550))
              screen.blit(ktc, (950, 550))
              pygame.display.flip()
              time.sleep(.03)
              if abs(thetaCab) > 2*pi:
                     thetaCab -= 2*pi*thetaCab/abs(thetaCab)
              if abs(thetaTruck) > 2*pi:
                     thetaTruck -= 2*pi*thetaTruck/abs(thetaTruck)
              print(thetaCab, thetaTruck)




       
