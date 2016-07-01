#ready! set! race!
import pygame, math

pygame.init()
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
white = 255,255,255
black = 0, 0, 0
color = 255,255,0

font = pygame.font.SysFont("Comic Sans MS", 12)
track = []
print('StartLine!')
xa = int(input('x1'))
xb = int(input('x2'))
ya = int(input('y1'))
yb = int(input('y2'))
startLine = [xa,xb,ya,yb]
prevLine = startLine
screen.fill(white)
pygame.draw.line(screen, color, (startLine[0],startLine[2]), (startLine[1], startLine[3]), 2)
pygame.display.flip()
while(1):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys. exit()
    print('NewLine! previousend value was:', prevLine[1],prevLine[3])
    cont = input('continue side?')
    if cont == 'y':
        xa = prevLine[1]
        xb = int(input('newX'))
        ya = prevLine[3]
        yb = int(input('newY'))
    else:
        xa = input('x1')
        if xa == 'n':
            break
        else: xa = int(xa)
        xb = int(input('x2'))
        ya = int(input('y1'))
        yb = int(input('y2'))
    line = [xa,xb,ya,yb]

    pygame.draw.line(screen, black, (line[0],line[2]), (line[1], line[3]), 2)
    pygame.display.flip()
    approve = input('keep? (y/n)')
    if approve == 'y':
        track.append(line)
        prevLine = line
        coord = font.render((str(line[1])+','+str(line[3])), 2, color)
        screen.blit(coord, (line[1],line[3]))
        
    else:
        pygame.draw.line(screen, white, (line[0],line[2]), (line[1], line[3]), 2)
save = input('save? (y/n)')
if save == 'y':
    fileName = input('file name? ')
    file = open(fileName, 'w')
    segmentString = str()
    for p in startLine:
        segmentString += str(p)
    segmentString += '\n'
    file.write(segmentString)
    for seg in track:
        segmentString = str()
        for p in seg:
            segmentString += str(p)
        segmentString += '\n'
        file.write(segmentString)
    file.close()
