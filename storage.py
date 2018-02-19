# command for get arduino type
arduinoInfoCommand = bytearray([0xF1])

# motor variable
motorValue = [False,False]
motor = [0,0,0,0,0,0]

#depth, yaw, (pitch, roll) received variable from arduino
depth = 0
yaw = 0
pitch = 0
row = 0
pitchPid = False
yawPid = False
yawSetPoint = 0

stage = [False,False,False,False] # representing stage 1, 2, 3, 4

qualification = False # whether or not in qualifying round

dataBuffer = [] # Data buffer that sending to arduino

def initialize():
    global motorValue, motor, depth, yaw, pitch, row, pitchPid, yawPid, yawSetPoint, stage, dataBuffer
    motorValue = [False,False]
    motor = [0,0,0,0,0,0]
    depth = 0
    yaw = 0
    pitch = 0
    row = 0
    pitchPid = False
    yawPid = False
    yawSetPoint = 0
    stage = [False,False,False,False]
    dataBuffer = []
