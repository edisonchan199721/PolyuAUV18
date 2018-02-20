# command for get arduino type
arduinoInfoCommand = bytearray([0xF1])

# motor variable
motorValue = [False,False]
motor = [0,0,0,0,0,0]

#depth, yaw, (pitch, roll) received variable from arduino
depth = 0
yaw = 0
pitch = 0
roll = 0
pitchPid = False
yawPid = False
yawSetPoint = 0
initalYaw = 0
initalDepth = 0
initalPitch = 0

stage = [False,False,False,False] # representing stage 1, 2, 3, 4

qualification = False # whether or not in qualifying round

dataBuffer = [] # Data buffer that sending to arduino

def reset():
    global motorValue, motor, depth, yaw, pitch, roll, pitchPid, yawPid, yawSetPoint, stage, dataBuffer, initalYaw, initalDepth, initalPitch 
    motorValue = [False,False]
    motor = [0,0,0,0,0,0]
    depth = 0
    yaw = 0
    pitch = 0
    roll = 0
    pitchPid = False
    yawPid = False
    yawSetPoint = 0
    initalYaw = 0
    initaldepth = 0
    initalPitch = 0
    stage = [False,False,False,False]
    dataBuffer = []
