#orbital sandbox
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
green = 0,255,0
orange = 255,153, 51
grey = 160, 160, 160
yellow = 255,255,0
colors = {'white': white, 'black': black, 'blue': blue, 'red': red, 'green': green, 'orange': orange, 'grey': grey,
          'yellow': yellow}
screen = pygame.display.set_mode(size)
SF = 1
#step = 86400
step = 5

G = 6.67e-11

font = pygame.font.SysFont("Comic Sans MS", 10)


def terminal(x):
       terminalF = (x)*(x+1)/2
       return terminalF

def gravitate(bodies):
       nF = len(bodies) - 1
       Forces = list()
       for n in range(0, len(bodies)):
              bodyForces = list()
              for n in range(0, nF):
                     bodyForces.append([0,0])
              Forces.append(list(bodyForces))
       for i in range(0, nF):
              for j in range((i+1), len(bodies)):
                     x = bodies[j][1] - bodies[i][1]
                     y = bodies[j][2] - bodies[i][2]
                     r = math.hypot(x, y)
                     if r == 0:
                            r = 1
                     theta = math.atan2(y, x)
                     #universal greavitation with scaling factor
                     f = ((G)*(bodies[i][3])*(bodies[j][3]))/(r**2)
                     Fx = f*math.cos(theta)
                     Fy = f*math.sin(theta)
                     Forces[i][(j-1)][0] = Fx
                     Forces[i][(j-1)][1] = Fy
                     #equal and opposite
                     Forces[(j)][i][0] = -1*Fx
                     Forces[(j)][i][1] = -1*Fy

       return Forces
                     
def sumForces(forces):
       xy =[0,0]
       Force = list()
       for i  in range(0, len(forces)):
              Force.append(list(xy))
              fx = 0
              fy = 0
              for j in range(0, len(forces[i])):
                     fx += forces[i][j][0]
                     fy += forces[i][j][1]
              Force[i][0] = fx
              Force[i][1] = fy

       return Force

def accelerate(bodies, force, step):
       for i in range(0, len(bodies)):
              Ax = force[i][0]/bodies[i][3]
              Ay = force[i][1]/bodies[i][3]
              
              bodies[i][4] += Ax*step
              bodies[i][5] += Ay*step
              #print(bodies[i][0], force[i][0], force[i][1])
       return bodies

def move(bodies, step):
       for i in range(0, len(bodies)):
              bodies[i][1] += bodies[i][4]*step
              bodies[i][2] += bodies[i][5]*step
       return bodies

def draw(bodies):
       global scale
       for i in range(0, len(bodies)):
              #print(bodies[i])
              yscale = (scale)
              xscale = (scale)*(width/height)
              cx = width*bodies[i][1]/(xscale) + (width/2)
              cy = (height*bodies[i][2])/(yscale) + (height/2)
              center = [int(cx), int(cy)]
              radius = int(bodies[i][6])
              label = font.render(bodies[i][0], 2, red)
              #print(center, radius)
              pygame.draw.circle(screen, bodies[i][7], center, radius)
              screen.blit(label, (center))
              pygame.display.flip()
       

                                
              
def addBody():
       global cast, scale, center
       print('New Body')
       label = str(input('BodyLabel--'))
       if label == 'Sun':
              yn = input('Central body? (y/n)')
              if yn == 'y':
                     body = ['Sun', 0.0, 0.0, 2e30, 0.0, 0.0, 30, yellow]
              else:
                     Xi = float(input('Xpos--'))
                     Yi = float(input('Ypos--'))
                     Vx = float(input('Velocity in X direction--'))
                     Vy = float(input('Velocity in Y direction--'))
                     body = ['Sun', Xi, Yi, 2e30, Vx, Vy, 30, yellow]
       elif label == 'Earth':
              yn = input('Central body? (y/n)')
              if yn == 'y':
                     body = ['Earth', 0.0, 0.0, 6e24, 0.0, 0.0, 20, blue]
                     center = 'Earth'
              else:
                     yn = input('heliocentric? (y/n)')
                     if yn == 'y':
                            body = ['Earth', 152e9, 0.0, 6e24, 0.0, 30e3, 10, blue]
                            center = 'Sun'
                     else:
                            Xi = float(input('Xpos--'))
                            Yi = float(input('Ypos--'))
                            Vx = float(input('Velocity in X direction--'))
                            Vy = float(input('Velocity in Y direction--'))
                            body = ['Earth', Xi, Yi, 6e24, Vx, Vy, 10, blue]
       elif label == 'Moon':
              body = ['Moon', (152e9) + (384399e3), 0.0, 7.34767309e22, 0.0, ((1.023e3) + (30075)), 2, grey]
       elif label == 'ISS':
              body = ['ISS', 6771000, 0.0, 370000, 0.0, 7670.018, 5, orange]
       elif label == 'Mercury':
              body = ['Mercury', 57.91e9, 0.0, 328.5e21, 0.0, 47.36e3, 10, grey]
       elif label == 'Venus':
              body = ['Venus', 108.2e9, 0.0, 4.87e24, 0.0, 35.02e3, 10, orange]
       elif label == 'Mars':
              body = ['Mars', 227.9e9, 0.0, 639e21, 0.0, 24.13e3, 10, red]
       else:
              addType = input('add type: (v)alue,  (e)ccentricity')
              if addType == 'v':
                     Xi = float(input('Xpos--'))
                     Yi = float(input('Ypos--')) 
                     M = float(input('Mass--'))
                     Vx = float(input('Velocity in X direction--'))
                     Vy = float(input('Velocity in Y direction--'))
              elif addType == 'e':
                     found = 0
                     while found != 1:

                            for i in range(0, len(cast)):
                                   if center == cast[i][0]:
                                          found = 1
                                          cindex = int(i)
                                   else:
                                          found = 0
                                                 
                     xc = cast[cindex][1]
                     yc = cast[cindex][2]
                     mc = cast[cindex][3]
                     vxc = cast[cindex][4]
                     vyc = cast[cindex][5]
                     Rp = float(input('periapsis distance?'))
                     e = float(input('eccentricity?'))
                     a = Rp/(1-e)
                     M = float(input('Mass--'))
                     mu= G*(mc + M)
                     V = math.sqrt(mu*((2/Rp)-(1/a)))

                     Xi = xc + Rp
                     Yi = yc
                     Vx = vxc
                     Vy = vyc + V
                     
              r = float(input('radius(arbitrary)--'))
              inputcolor = input('color--')
              if inputcolor in colors:
                     color = colors[inputcolor]
              else:
                     print('Not a valid color')
                     print('Color set to orange')
                     color = orange
                            
              body = [label, Xi, Yi, M, Vx, Vy, r, color]
       cast.append(body)

       
add = 1
cast = list()
print('All dimensions in base units (m, m/s, kg)')
print('powers of ten can be entered as 1e2 for 100')
while add != 'n':
       addBody()
       add = input('Add another body? (y/n)')

print('please enter width of window in Au')
viewscale = input('window scale-- (solar/geo/custom)')
if viewscale == 'solar':
       scale = 6.0
elif viewscale == 'geo':
       scale = 1e-4
else:
       scale = float(viewscale)

scale = scale*149597871000
time.sleep(3)


while(1):
       draw(cast)
       Forces = gravitate(cast)
       Force = sumForces(Forces)
       cast = accelerate(cast, Force, step)
       cast = move(cast, step)
       screen.fill(white)
       
       
       
              
              


