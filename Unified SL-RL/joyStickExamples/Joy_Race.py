#Ready! Set! Race!
#race controlled by joystick

import pygame, sys, race, math, time
from pygame.locals import *
pi = math.pi

pygame.init()

size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont("Comic Sans MS", 12)
FailFont  = pygame.font.SysFont("Comic Sans MS", 60)
red = 255,0,0

L = 40
W = 20

track, startLine = race.openTrack('stadium')
print(len(track))
start_theta = (pi/2) + math.atan2((startLine[2]-startLine[0]),(startLine[3]-startLine[1]))
start_x  = 0.5*(startLine[0]+startLine[1])
start_y  = 0.5*(startLine[2]+startLine[3])

print(start_x, start_y, start_theta)
trackPoly = race.SegToPoly(track, 2)

car = race.vehicle(start_x,start_y,start_theta, L, W)
speed = 3
sensor_list = [-90,-60,-30,0,30,60,90]
senseProx = [0]*len(sensor_list)
R = 60 #sensor range



### Tells the number of joysticks/error detection
joystick_count = pygame.joystick.get_count()
print ("There is ", joystick_count, "joystick/s")
if joystick_count == 0:
       print ("Error, I did not find any joysticks")
else:
       my_joystick = pygame.joystick.Joystick(0)
       my_joystick.init()
       
while True:
       go = 0
       no = 0
       while go == 0:
              for event in pygame.event.get():
                     if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
              go = my_joystick.get_button(0)
              no = my_joystick.get_button(1)
              if no != 0:
                     break
                     
              
       while True:
              race.drawRace(screen, car, trackPoly, startLine, sensor_list, senseProx, R)
              for event in pygame.event.get():
                     if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
              n_steer = my_joystick.get_axis(0)
              n_speed = my_joystick.get_axis(1)
              speed = -math.copysign(1,n_speed)*5*n_speed**2
              steer = 20*(n_steer)- 1.4685
              car = race.drive(car,speed,steer)
              senseProx  = race.proximity(track, car, sensor_list, R)
              time.sleep(0.04)
              if senseProx == 'crash':
                     break
       print('Crash!')
       crash = FailFont.render('Crash!', 5, red)
       screen.blit(crash,(int(width/2),int(height/2)) )
       pygame.display.update()
              
       car = race.vehicle(start_x,start_y,start_theta, L, W)
       senseProx = [0]*len(sensor_list)
              
              
              
                     
                     
              
