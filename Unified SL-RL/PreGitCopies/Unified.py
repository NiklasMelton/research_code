#unified method
#from scratch

import pygame, math, Neural, race, sys, time, random
from pygame.locals import *


pygame.init()

pi = math.pi
L = 40
W = 20
joy_bias = 0.065
LR = 0.3
dconst = 0.1
a_Xlen = 8
a_Ylen = 4
a_Zlen = 1
#weights set up
a_A = []
for y in range(0,a_Ylen):
       a_A.append([])
       for x in range(0,a_Xlen):
              a_A[y].append(random.uniform(-1.0,1.0))
a_B = []
for z in range(0,a_Zlen):
       a_B.append([])
       for y in range(0,a_Ylen):
              a_B[z].append(random.uniform(-1.0,1.0))

m_Xlen = 9
m_Ylen = 10
m_Zlen = 8
m_A = []
for y in range(0,m_Ylen):
       m_A.append([])
       for x in range(0,m_Xlen):
              m_A[y].append(random.uniform(-1.0,1.0))
m_B = []
for z in range(0,m_Zlen):
       m_B.append([])
       for y in range(0,m_Ylen):
              m_B[z].append(random.uniform(-1.0,1.0))
c_Xlen = 9
c_Ylen = 6
c_Zlen = 1

#Menu----------------------
print('--------------------INPUT REQUIRED--------------------')       
K = float(input('Critic trust (K) = ')) 
LCF = input('Load Critic File?')
if LCF == 'y':
       c_A = []
       criticFile = open('critic_file', 'r')
       for y in range(0, c_Ylen):
              c_A.append([])
              for x in range(0, c_Xlen):
                     c_A[y].append(float(criticFile.readline()))
       c_B = []
       for z in range(0, c_Zlen):
              c_B.append([])
              for y in range(0, c_Ylen):
                     c_B[z].append(float(criticFile.readline()))
       criticFile.close()
else:
       c_A = []
       for y in range(0, c_Ylen):
              c_A.append([])
              for x in range(0, c_Xlen):
                     c_A[y].append(random.uniform(-1.0,1.0))
       c_B = []
       for z in range(0, c_Zlen):
              c_B.append([])
              for y in range(0, c_Ylen):
                     c_B[z].append(random.uniform(-1.0,1.0))
       


              
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont("Comic Sans MS", 10)
FailFont  = pygame.font.SysFont("Comic Sans MS", 60)
red = 255,0,0


track, startLine = race.openTrack('stadium')

start_theta = (pi/2) + math.atan2((startLine[2]-startLine[0]),(startLine[3]-startLine[1]))
start_x  = 0.5*(startLine[0]+startLine[1])
start_y  = 0.5*(startLine[2]+startLine[3])
trackPoly = race.SegToPoly(track, 2)

car = race.vehicle(start_x,start_y,start_theta, L, W)
track_angle = math.atan2((start_y-(height/2)),(start_x-(width/2)))
n_theta = Neural.normalize(track_angle,0,pi*2,1)

speed = 3
sensor_list = [-90,-60,-30,0,30,60,90]
senseProx = [0]*len(sensor_list)
R = 60 #sensor range



#Tells the number of joysticks/error detection
joystick_count = pygame.joystick.get_count()
print ("There is ", joystick_count, "joystick/s")
if joystick_count == 0:
       print ("Error, I did not find any joysticks")
else:
       print('Joystick found')
       my_joystick = pygame.joystick.Joystick(0)
       my_joystick.init()
    
while True:
       print('pause game to save at any time')
       print('Press A to play/pause, B to quit, start to save')
       go = 0
       no = 0
       car = race.vehicle(start_x,start_y,start_theta, L, W)
       n_theta_old = n_theta
       
       while go == 0:
              for event in pygame.event.get():
                     if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
              
              go = my_joystick.get_button(0)
              if my_joystick.get_button(1) == 1: break
              if  my_joystick.get_button(9) == 1:
                     File = open('actor_file', 'w')
                     for a in range(0, len(a_A)):
                            for b in range(0, len(a_A[a])):
                                   File.write(str(a_A[a][b])+'\n')
                     for a in range(0, len(a_B)):
                            for b in range(0, len(a_B[a])):
                                   File.write(str(a_B[a][b])+'\n')
                     File.close()
                     File = open('model_file', 'w')
                     for a in range(0, len(m_A)):
                            for b in range(0, len(m_A[a])):
                                   File.write(str(m_A[a][b])+'\n')
                     for a in range(0, len(m_B)):
                            for b in range(0, len(m_B[a])):
                                   File.write(str(m_B[a][b])+'\n')
                     File.close()
                     File = open('critic_file', 'w')
                     for a in range(0, len(c_A)):
                            for b in range(0, len(c_A[a])):
                                   File.write(str(c_A[a][b])+'\n')
                     for a in range(0, len(c_B)):
                            for b in range(0, len(c_B[a])):
                                   File.write(str(c_B[a][b])+'\n')
                     File.close()
                     
       car = race.drive(car,speed,0)              
       senseProx  = race.proximity(track, car, sensor_list, R)
       track_angle = math.atan2((start_y-(height/2)),(start_x-(width/2)))
       n_theta = Neural.normalize(track_angle,0,pi*2,1)
       Rstate = []
       for s in senseProx:
              Rstate.append(s)
       Rstate.append(n_theta)
       while True:
              for event in pygame.event.get():
                     if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
              race.drawRace(screen, car, trackPoly, startLine, sensor_list, senseProx, R)
              #Pause Menu----------------------
              if my_joystick.get_button(0) == 1:
                     print('Paused -- press A to continue or start to save')
                     time.sleep(0.2)
                     while go == 0:
                            if  my_joystick.get_button(9) == 1:
                                   File = open('actor_file', 'w')
                                   for a in range(0, len(a_A)):
                                          for b in range(0, len(a_A[a])):
                                                 File.write(str(a_A[a][b])+'\n')
                                   for a in range(0, len(a_B)):
                                          for b in range(0, len(a_B[a])):
                                                 File.write(str(a_B[a][b])+'\n')
                                   File.close()
                                   File = open('model_file', 'w')
                                   for a in range(0, len(m_A)):
                                          for b in range(0, len(m_A[a])):
                                                 File.write(str(m_A[a][b])+'\n')
                                   for a in range(0, len(m_B)):
                                          for b in range(0, len(m_B[a])):
                                                 File.write(str(m_B[a][b])+'\n')
                                   File.close()
                                   File = open('critic_file', 'w')
                                   for a in range(0, len(c_A)):
                                          for b in range(0, len(c_A[a])):
                                                 File.write(str(c_A[a][b])+'\n')
                                   for a in range(0, len(c_B)):
                                          for b in range(0, len(c_B[a])):
                                                 File.write(str(c_B[a][b])+'\n')
                                   File.close()

              #Unified learning--------------------------
              
              #Run Actor network
              a_X = Rstate
              a_Y, a_steer = Neural.feedForward(a_X, a_A, a_B)
              #input human control
              j_steer = Neural.normalize(my_joystick.get_axis(0),-1,1) - joy_bias
              
              #model next states for both actions
              a_mX = []
              h_mX = []
              for r in Rstate:
                     a_mX.append(r)
                     h_mX.append(r)
              a_mX.append(a_steer)
              h_mX.append(j_steer)
              a_mY, aState_next = Neural.feedForward(a_mX, m_A, m_B)
              h_mY, hState_next = Neural.feedForward(h_mX, m_A, m_B)

              a_cX=[]      
              for i in aState_next:
                     a_cX.append(i)
              a_cX.append(n_theta)
              h_cX=[]      
              for i in hState_next:
                     h_cX.append(i)
              h_cX.append(n_theta)
              

              #Critique the future state
              a_cY, a_crit = Neural.feedForward(a_cX, c_A, c_B)
              h_cY, h_crit = Neural.feedForward(h_cX, c_A, c_B)


              #Update Actor                  
              #through critic
              h_cdz = (h_crit)*(h_crit*(1-h_crit)+dconst)
              a_cdz = (a_crit)*(a_crit*(1-a_crit)+dconst)
              h_mdz = Neural.backpropogate(h_cX, c_A, h_cY, c_B, h_cdz)
              a_mdz = Neural.backpropogate(a_cX, c_A, a_cY, c_B, a_cdz)
              h_mdz.pop(len(h_mdz)-1)
              a_mdz.pop(len(a_mdz)-1)
              #through model
              h_dz = Neural.backpropogate(hState_next, m_A, h_mY, m_B, h_mdz)
              a_dz = Neural.backpropogate(aState_next, m_A, a_mY, m_B, a_mdz)
              #isolate control variable
              h_dsteer = h_dz[(len(h_dz)-1)]
              a_dsteer = a_dz[(len(a_dz)-1)]
              #Find Supervised Learning delta
              SL_dsteer = (a_steer*(1-a_steer)+dconst)*(a_steer - j_steer)
              #Combine learning methods
              dsteer = (K*(a_dsteer) + (1-K)*(SL_dsteer + K*h_dsteer))
              #Update Actor weights
              a_da, a_db = Neural.backpropogate(a_X, a_A, a_Y, a_B, dsteer, 1)
              for j in range(0, len(a_da)):
                     for i in range(0, len(a_da[j])):
                            a_A[j][i] -= LR*a_X[i]*a_da[j][i]
              for k in range(0, len(a_db)):
                     for j  in range(0, len(a_db[k])):
                            a_B[k][j] -= LR*a_Y[j]*a_db[k][j]
              

              #move using joystick input
              n_theta_old = n_theta
              steer = (j_steer*40)-20
              car = race.drive(car,speed,steer)
              n_theta = Neural.normalize(car[2],0,2*pi,1)
              senseProx  = race.proximity(track, car, sensor_list, R)
              if senseProx == 'crash':
                     break

              

              #Update Model
              Rstate = []
              m_dz = []
              for s in senseProx:
                     Rstate.append(s)
                     m_dz.append(0)
              m_dz.append(0)       
              Rstate.append(n_theta)
              for i in range(0, len(Rstate)):
                     m_dz[i] = (hState_next[i]*(1-hState_next[i])+dconst)*(hState_next[i] - Rstate[i])
              m_da, m_db = Neural.backpropogate(h_mX, m_A, h_mY, m_B, m_dz, 1)
              for j in range(0, len(m_da)):
                     for i in range(0, len(m_da[j])):
                            m_A[j][i] -= LR*h_mX[i]*m_da[j][i]
              for k in range(0, len(m_db)):
                     for j  in range(0, len(m_db[k])):
                            m_B[k][j] -= LR*h_mY[j]*m_db[k][j]

##              #Update Critic
##              Rstate.append(n_theta_old)
##              J_cY, J_crit = Neural.feedForward(Rstate, c_A, c_B)
##              U_crit = 0
##              for r in range(0, len(Rstate)-1):
##                     U_crit += 0.5*(Rstate[r]**2)
##              U_crit -= 0.5*((n_theta - n_theta_old)**2)
##              C_dz = (J_crit*(1-J_crit)+dconst)*(J_crit-U_crit)
##              c_da, c_db = Neural.backpropogate(Rstate, c_A, J_cY, c_B, C_dz, 1)
##              for j in range(0, len(c_da)):
##                     for i in range(0, len(c_da[j])):
##                            c_A[j][i] -= LR*Rstate[i]*c_da[j][i]
##              for k in range(0, len(c_db)):
##                     for j  in range(0, len(c_db[k])):
##                            c_B[k][j] -= LR*J_cY[j]*c_db[k][j]



              #print data
              data_out = [h_dsteer, a_dsteer, SL_dsteer, K]
              for a in range(0, len(data_out)):
                     posX = int(300)
                     posY = int(300+a*10)
                     screen.blit(font.render(str(data_out[a]), 2, red), (posX, posY))
              pygame.display.update()
              time.sleep(0.03)
              
       

              
              
              
                            
              
              
              
              
              

              
