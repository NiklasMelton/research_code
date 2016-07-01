#Simple truck driving program
#control the truck with the arrow keys. 
import sys, pygame, math, time, TruckSimulator as tsim

pygame.init()
pi = math.pi
size = width, height = 1000, 500
white = 255,255,255
red = 255,0,0
screen = pygame.display.set_mode(size)
goal = (0, int(height/2))
steer = 0
speed = 0
myTruck = tsim.truck(400, 255, (pi), 0, red)


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
       nsteer = math.radians(steer)
       tsim.drive(myTruck,speed,nsteer)
       tsim.drawTruck(myTruck,goal,screen,1)
       time.sleep(0.1)
       
