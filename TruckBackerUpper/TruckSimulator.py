#Truck Simulator
#Still requires external call of pygame.init() and pygame.event checking

#Begin by defining a truck(x,y,trailerAngle, cabAngle, color)
#the x,y cooridenents are absolute with respect to your screen
#both angles are in radians and are not confined to a range
#color should be in (255,255,255) form

#You can then call drive(truck,speed,steer) which will update your truck
#accordingly

#finally call drawTruck(truck,goal,screen,1)
#which will flash the screen with the updated drawing of the truck and
#will place a green dot at the (x,y) goal location. Adding the 1 removes the old
#trace and clears the screen.

import sys, pygame, math
pi = math.pi

class truck:
    #define a vehicle
    def __init__(self, xcoord, ycoord, TrailerAngle, CabAngle, color):
        #TrailerAngle = 0 points truck toward left screen in pygame
        #CabAngle is relative to the cabs neutral position WRT the trailer
        #all angles in radians
        self.x = float(xcoord)
        self.y = float(ycoord)
        self.TA = float(TrailerAngle)
        self.CA = float(CabAngle)
        self.w = 20
        self.LT = 80
        self.LC = 30
        self.C = color

def drive(vehicle, speed, steer):
    #defines kinematic motion of truck
    #vehicle is expected to be of class type truck
    #speed is arbitrary but +- 10 can be pretty quick with 0.1s refreshing
    #higher speed will lead to less accurate kinematic modeling
    #steer is expected in radians +- from neutral 
    #!!steer values exceeding the radian equivelent of +- 20 degrees
    #lead to jack-knifing while in reverse!!
    xTruck = vehicle.x
    yTruck = vehicle.y
    thetaTruck = vehicle.TA
    thetaCab = vehicle.CA
    xCab = xTruck - vehicle.LT*math.cos(-thetaTruck)
    yCab = yTruck - vehicle.LT*math.sin(thetaTruck)

    thetaCab += (speed*math.tan(steer)/vehicle.LC)
    xCab += (speed*math.cos(-thetaCab))
    yCab +=  (speed*math.sin(thetaCab))
    thetaTruck += (speed*math.sin(thetaTruck-thetaCab)/vehicle.LT)
    xTruck = xCab + vehicle.LT*math.cos(-thetaTruck)
    yTruck =  yCab + vehicle.LT*math.sin(thetaTruck)
    vehicle.x = xTruck
    vehicle.y = yTruck
    vehicle.TA = thetaTruck
    vehicle.CA = thetaCab


    return


def drawTruck(vehicle, goal, screen, scrnCLR = None):
    #expects class type truck
    #expects goal as two int list (x,y)
    if scrnCLR != None:
        screen.fill((255,255,255))
    xTruck = vehicle.x
    yTruck = vehicle.y
    thetaTruck = vehicle.TA
    thetaCab = vehicle.CA
    xCab = xTruck - vehicle.LT*math.cos(-thetaTruck)
    yCab = yTruck - vehicle.LT*math.sin(thetaTruck)
    xWheel = xCab + vehicle.LC*math.cos(thetaCab)
    yWheel = yCab + vehicle.LC*math.sin(thetaCab)
    pygame.draw.polygon(screen, vehicle.C, [(xCab,yCab),(xCab+(1.4*(vehicle.w/2))*math.cos(0.785398+thetaCab),yCab+(1.4*(vehicle.w/2))*math.sin(0.785398+thetaCab)), (xWheel-(vehicle.w/2)*math.sin(thetaCab), yWheel+(vehicle.w/2)*math.cos(thetaCab)), (xWheel +(vehicle.w/2)*math.sin(thetaCab), yWheel-(vehicle.w/2)*math.cos(thetaCab)), (xCab+(1.4*(vehicle.w/2))*math.cos(thetaCab-0.785399), yCab+(1.4*(vehicle.w/2))*math.sin(thetaCab-0.78539))], 2)
    pygame.draw.polygon(screen, vehicle.C, [(xTruck+(vehicle.w/2)*math.sin(-thetaTruck),yTruck+(vehicle.w/2)*math.cos(thetaTruck)),(xCab+(vehicle.w/2)*math.sin(-thetaTruck),yCab+(vehicle.w/2)*math.cos(thetaTruck)),(xCab-(vehicle.w/2)*math.sin(-thetaTruck),yCab-(vehicle.w/2)*math.cos(thetaTruck)),(xTruck-(vehicle.w/2)*math.sin(-thetaTruck),yTruck-(vehicle.w/2)*math.cos(thetaTruck))], 2)
    pygame.draw.circle(screen, (0,255,0), goal, 10)
    pygame.display.flip()
