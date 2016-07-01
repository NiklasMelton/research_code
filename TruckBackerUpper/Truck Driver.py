#truck driver

import sys, pygame
import sys, math
import sys, time
pygame.init()

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
xTruck = LTruck/2
yTruck = 300
thetaTruck = math.pi
thetaCab = .785
xCab = xTruck + LTruck 
yCab = 300
steer = 0
speed = 0

       
while(1):
       for event in pygame.event.get():
              if event.type == pygame.QUIT: sys. exit()
              if event .type == pygame.KEYDOWN:
                     if event.key == pygame.K_LEFT and steer > -18:
                            steer -= 2
                     if event.key == pygame.K_RIGHT and steer < 18:
                            steer += 2
                     if event.key == pygame.K_UP and speed < 22:
                            speed += 2
                     if event.key == pygame.K_DOWN and speed > -22:
                            speed -= 2
       steer = math.radians(steer)
       #kinematics
       thetaCab += (speed*math.tan(steer)/LCab)
       xCab += (speed*math.cos(-thetaCab))
       yCab +=  (speed *math.sin(thetaCab))
       thetaTruck +=  (speed*math.sin(thetaTruck-thetaCab)/LTruck)
       xTruck = xCab + LTruck*math.cos(-thetaTruck)
       yTruck =  yCab + LTruck*math.sin(thetaTruck)
       xWheel = xCab + LCab*math.cos(thetaCab)
       yWheel = yCab + LCab*math.sin(thetaCab)

       
       if abs(thetaCab > 2*math.pi):
              thetaCab -= 2*math.pi*thetaCab/abs(thetaCab)
       if thetaCab < 0:
              thetaCab += 2*math.pi
       nthetaTruck = thetaTruck
       if abs(nthetaTruck > 2*math.pi):
              nthetaTruck -= 2*math.pi*thetaTruck/abs(thetaTruck)
       if nthetaTruck < 0:
              nthetaTruck += 2*math.pi
       
       nthetaCab = (thetaCab-nthetaTruck-math.pi)
       if abs(nthetaCab) > math.pi:
              nthetaCab -= 2*math.pi*nthetaCab/abs(nthetaCab)

       #draw truck then turn indicator
       screen.fill(white)
       #pygame.draw.lines(screen, black, False, [(xTruck,yTruck),(xCab,yCab),(xWheel,yWheel)], 5)
       pygame.draw.polygon(screen, red, [(xCab,yCab),(xCab+14*math.cos(0.785398+thetaCab),yCab+14*math.sin(0.785398+thetaCab)), (xWheel-10*math.sin(thetaCab), yWheel+10*math.cos(thetaCab)), (xWheel +10*math.sin(thetaCab), yWheel-10*math.cos(thetaCab)), (xCab+14*math.cos(thetaCab-0.785399), yCab+14*math.sin(thetaCab-0.78539))])
       pygame.draw.polygon(screen, red, [(xTruck+10*math.sin(-thetaTruck),yTruck+10*math.cos(thetaTruck)),(xCab+10*math.sin(-thetaTruck),yCab+10*math.cos(thetaTruck)),(xCab-10*math.sin(-thetaTruck),yCab-10*math.cos(thetaTruck)),(xTruck-10*math.sin(-thetaTruck),yTruck-10*math.cos(thetaTruck))])
       pygame.draw.rect(screen, red, (450, 40, 90, 20))
       steer = int(math.degrees(steer))
       pygame.draw.circle(screen,blue,(int(495+steer), 50), 15)
       pygame.display.flip()
       time.sleep(.03)

       normTT = thetaTruck/math.pi
       normTC = thetaCab/math.pi
       print(math.degrees(nthetaCab), math.degrees(nthetaTruck), )








       
