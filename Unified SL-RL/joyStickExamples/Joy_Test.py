#joyTest

import pygame, sys
pygame.init()

size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont("Comic Sans MS", 12)
pos = [int(width/2),int(height/2)]
joystick_count = pygame.joystick.get_count()

my_joystick = pygame.joystick.Joystick(0)
my_joystick.init()
while True:
    screen.fill((255,255,255))
    pygame.draw.circle(screen,(255,0,0), (pos), 50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    h_axis = my_joystick.get_axis(0)
    button = []
    for b in range(0,8):
        button.append([my_joystick.get_button(b),b])
    print(button)
    #if h_axis < 0: h_axis = 0
    #if h_axis > maxAxis: h_axis = maxAxis
    n_steer = h_axis
    pos[0] += int(n_steer*10)
    pygame.display.update()
