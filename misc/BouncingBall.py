#pygame simple test

import sys, pygame
pygame.init()

size = width, height = 400, 400
radius = 10
speed = [1,1]
black = 0,0,0
color = 0,255,0

x = 20
y = 150

screen = pygame.display.set_mode(size)

while(1):
       for event in pygame.event.get():
              if event.type == pygame.QUIT: sys. exit()

       x = x + speed[0]
       y = y + speed[1]

       if  x+radius >width or x - radius < 0:
              speed[0] = -1*speed[0]
       if y + radius > height or y - radius < 0:
              speed[1] = -1*speed[1]

       screen.fill(black)
       pygame.draw.circle(screen, color, (x,y),radius)
       pygame.display.flip()
       

       




       
