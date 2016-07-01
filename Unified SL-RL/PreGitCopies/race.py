#ready! set! race!
import pygame, sys, math

def openTrack(trackFile):
    #imports track as a file listing lines of 3 digit coordinates in sets of 4.
    #corasponding to [x1,x2,y1,y2]
    #converts this file to an object with same coordinate system
    file = open(trackFile, 'r')
    track  = []
    n = 0
    
    for i in file:
        line = str(i)
        if n == 0:
            startLine = [int(line[0:3]),int(line[3:6]),int(line[6:9]), int(line[9:12])]
            n+=1
        else:
            segment = [int(line[0:3]),int(line[3:6]),int(line[6:9]), int(line[9:12])]
            track.append(segment)
    return track, startLine

def newTrack():
    pygame.init()
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    white = 255,255,255
    black = 0, 0, 0
    red = 255,0,0

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
    pygame.draw.line(screen, red, (startLine[0],startLine[2]), (startLine[1], startLine[3]), 2)
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
            coord = font.render((str(line[1])+','+str(line[3])), 2, red)
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

    return
    
            
def vehicle(x,y,theta,L,W):
    return [x,y,theta,L,W]

def proximity(track, vehicle, sensors, Range):
    #expects track object in form of [x1,x2,y1,y2]
    #vehicle in the form of [x,y,theta,L,W] theta in radians
    #sensors should list all sensor angles in degrees wrt theta zero
    #i.e. [-90,-60,-30,0,30,60,90]
    #returns max proximity from1-0 (close-far) for all sensors

    senseProx = [0]*len(sensors)
    n = 0
    for s in sensors:
        senseAngle = math.radians(s) + vehicle[2]
        a = 0
        for segment in track:
            if segment[0] < segment[1]:
                linexMin = segment[0]
                linexMax = segment[1]
            else:
                linexMin = segment[1]
                linexMax = segment[0]
            if segment[2] < segment[3]:
                lineyMin = segment[2]
                lineyMax = segment[3]
            else:
                lineyMin = segment[3]
                lineyMax = segment[2]
            if abs(segment[1]-segment[0]) > 0:
                
                m = (segment[3]-segment[2])/(segment[1]-segment[0])
                b = segment[2] - m*segment[0]
                if m == 0 and math.sin(senseAngle) == 0: prox = 0
                else:
                    R = ((b + m*vehicle[0] - vehicle[1])/(math.sin(senseAngle)-m*math.cos(senseAngle)))
                    xhit = R*math.cos(senseAngle) + vehicle[0]
                    yhit = m*xhit + b
                    if (xhit < linexMax and xhit > linexMin and R >0):
                        prox = 1 - (R/Range)
                    else: prox = 0
            else:
        
                xhit = segment[0]
                R = ((xhit-vehicle[0])/math.cos(senseAngle))
                yhit = R*math.sin(senseAngle) +vehicle[1]
                if (yhit < lineyMax and yhit > lineyMin and R >0):
                    prox = 1 - (R/Range)
                else: prox = 0
            a+=1
                
            
            if prox > senseProx[n]:
                senseProx[n] = prox
            
        n+=1
    crash = 0
    for s in senseProx:
        if s > 0.9:
            crash = 1
    if crash == 1:
        return 'crash'
    
    else:
        return senseProx
                   



def drive(vehicle, speed, steer):
    #defines kinematic motion of car
    #vehicle in the form of [x,y,theta, L, W] theta in radians
    #speed should be less than 10
    #steer should be in radians and is refrenced from the cars centerline
    #returns updated vehicle object state
    L = vehicle[3]
    r_steer = math.radians(steer)
    newState = [0]*len(vehicle)
    xb = vehicle[0] - L*math.cos(vehicle[2])
    yb = vehicle[1] - L*math.sin(vehicle[2])
    newState[2] = vehicle[2] + (speed*math.tan(r_steer))/L
    xb += (speed*math.cos(-newState[2]))
    yb += (speed*math.sin(newState[2]))
    newState[0] = xb + L*math.cos(newState[2])
    newState[1] = yb + L*math.sin(newState[2])
    newState[3] = vehicle[3]
    newState[4] = vehicle[4]
    return newState

def SegToPoly(segments, polyNum):
    poly = []
    for n in range(0, polyNum):
        poly.append([])
        for i in range(0, int(len(segments)/polyNum)):
            poly[n].append(0)
        
    
    n = 0
    i = 0
    for seg in segments:
        point = (seg[0], seg[2])
        endPoint = (seg[1], seg[3])
        if i == 0:
            poly[n][0] = point
            i += 1
        else:
            if (endPoint == poly[n][0]) and (n <  (polyNum)):
                poly[n][i] = point
                i = 0
                n += 1
            else :
                poly[n][i] = point
                
                
                i+=1
                
    return poly
            
    

def drawRace(screen, vehicle, trackPoly, startLine, sensors = None, senseProx = None, Range = None):
    white = 255,255,255
    black = 0, 0, 0
    yellow = 255,255,0
    red = 255,0,0
    screen.fill(white)
    xf = vehicle[0]
    yf = vehicle[1]
    xb = xf - vehicle[3]*math.cos(vehicle[2])
    yb = yf - vehicle[3]*math.sin(vehicle[2])
    xRect = 0.5*vehicle[4]*math.sin(-vehicle[2])
    yRect = 0.5*vehicle[4]*math.cos(-vehicle[2])
    xLB = xb + xRect 
    yLB = yb + yRect
    xRB = xb - xRect
    yRB = yb - yRect
    xLF = xf + xRect
    yLF = yf + yRect
    xRF = xf - xRect
    yRF = yf - yRect
    pygame.draw.line(screen, red, (startLine[0],startLine[2]), (startLine[1], startLine[3]), 3)
    pygame.draw.polygon(screen, red, [(xLB,yLB),(xRB,yRB),(xRF,yRF),(xLF,yLF)])
    pygame.draw.polygon(screen,black,trackPoly[0],2)
    pygame.draw.polygon(screen,black,trackPoly[1],2)
    
    if sensors != None:
        for s in range(0, len(sensors)):
            sAngle = vehicle[2] + math.radians(sensors[s])
            pygame.draw.line(screen, red, (xf,yf), ((xf+(Range*(1-senseProx[s])*math.cos(sAngle))), yf+(Range*(1-senseProx[s])*math.sin(sAngle))),2)

    pygame.display.flip()
        
    return        
        
    

    
    
                    

            
            
            

        
                
        

                
