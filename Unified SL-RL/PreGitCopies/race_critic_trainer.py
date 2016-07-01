import math, Neural, random

pi = math.pi
c_Xlen = 9
c_Ylen = 6
c_Zlen = 1
LR = 0.3
dconst = 0.1

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


avgerror = 1
thresh = 0.9
n = 0
while avgerror > 0.0002:
    #LR = Neural.sigmoid(3*avgerror)
    n+=1
    U_crit = 0
    sense_state = []
    for x in range(0, c_Xlen-2):
        sense_state.append(random.uniform(0.0,1.0))
    randAngle = random.uniform(0.0,1.0)
    randDiff = random.uniform(0.0,1.0)*0.1
    randAngleOld = Neural.normalize((randAngle - randDiff),0.0,1.0,1)

    Rstate = []
    Rstate = list(sense_state)
    Rstate.append(randAngle)
    Rstate.append(randAngleOld)
    R_cY, R_crit = Neural.feedForward(Rstate, c_A, c_B)
    for r in range(0, len(Rstate)):
        U_crit += 0.5*(Rstate[r]**2)
    U_crit -= 0.5*((randDiff)**2)
    U_crit = U_crit/(0.5*(1+len(Rstate)))
    error = 0.5*(R_crit-U_crit)**2
    avgerror = ((avgerror*20)+error)/21
    C_dz = (R_crit*(1-R_crit)+dconst)*(R_crit-U_crit)
    c_da, c_db = Neural.backpropogate(Rstate, c_A, R_cY, c_B, C_dz, 1)
    for j in range(0, len(c_da)):
        for i in range(0, len(c_da[j])):
            c_A[j][i] -= LR*c_da[j][i]
    for k in range(0, len(c_db)):
        for j  in range(0, len(c_db[k])):
            c_B[k][j] -= LR*c_db[k][j]
    if avgerror < thresh:
        print(avgerror,'--', n)
        thresh = 0.9*thresh
            
print('saving')
File = open('critic_file', 'w')
for a in range(0, len(c_A)):
      for b in range(0, len(c_A[a])):
             File.write(str(c_A[a][b])+'\n')
for a in range(0, len(c_B)):
      for b in range(0, len(c_B[a])):
             File.write(str(c_B[a][b])+'\n')
File.close()

              
    
