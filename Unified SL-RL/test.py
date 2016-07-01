import pygame
pygame.init()

my_joystick = pygame.joystick.Joystick(0)
my_joystick.init()
a = 8
button = [0]*a
while True:
    for i in range(0,a):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                   pygame.quit()
                   sys.exit()
        button[i] = my_joystick.get_button(i)
    print(button)

    
    
