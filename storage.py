import time

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
depthPid = False
pitchPid = False
yawPid = False
yawSetPoint = 0
initialYaw = 0
initialDepth = 0
initialPitch = 0
voltage = 0
current = 0

stage = [False,False,False,False] # representing stage 1, 2, 3, 4

qualification = False # whether or not in qualifying round

dataBuffer = [] # Data buffer that sending to arduino

end = False # end of the whole program

#image processing


def reset():
    global motorValue, motor, depth, yaw, pitch, roll, pitchPid, yawPid, yawSetPoint, stage, dataBuffer, initialYaw, initialDepth, initialPitch, voltage, current
    motorValue = [False,False]
    motor = [0,0,0,0,0,0]
    depth = 0
    yaw = 0
    pitch = 0
    roll = 0
    pitchPid = False
    yawPid = False
    yawSetPoint = 0
    initialYaw = 0
    initialdepth = 0
    initialPitch = 0
    stage = [False,False,False,False]
    dataBuffer = []
    voltage = 0
    current = 0

def initialVariable():
    global depth, yaw, pitch, initialYaw, initialDepth, initialPitch
    while not (len(dataBuffer)==0):
        time.sleep(0.1)
    initialYaw = yaw
    initialDepth = depth
    initialPitch = pitch
    print("initialYaw:",initialYaw,"initialDepth:",initialDepth,"initialPitch",initialPitch)
