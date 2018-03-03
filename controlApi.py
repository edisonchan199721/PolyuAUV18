import struct
import storage as storage

# Arduino no.0

setDepthByte = [0xA1] # short depth_setPoint [3 bytes]	(depth unit : cm)

setPitchByte = [0xA3]

setDepthPidOnByte = [0xAB]

calDepthByte = [0xAC]

setPitchPidOnByte = [0xAD]

getPitchRollByte = [0xFA]

getThruster2Byte = [0xFB]

getDepthByte = [0xFE]

getDepthPitchPidByte = [0xF4]

# Arduino no.1

moveByte = [0xB1] # short angle + byte magnitude [4 bytes] (angle: From -180 to 180 degree , magnitude : 0 - 255)

setYawByte = [0xB3]

setYawPidOnByte = [0xB7]

getYawByte = [0xFC]

getThruster4Byte = [0xFD]

getYawValueByte = [0xFF]

# Arduino no.2

getPowerByte = [0xEA]

setMagByte = [0xC1]

sendToArduino0 = [0xA1,0xA3,0xAB,0xAC,0xAD,0xF4,0xFA,0xFB,0xFE]
sendToArduino1 = [0xB1,0xB3,0xB7,0xFC,0xFD,0xFF]
sendToArduino2 = [0xEA,0xC1]

def move(angle,magnitude):
    command = []
    command += moveByte
    command += struct.pack('h',int(angle))
    command += struct.pack('B',int(magnitude))
    storage.dataBuffer.append(command[0:4])

def setDepth(depth):
    command = []
    command += setDepthByte
    command += struct.pack('h',int(depth))
    storage.dataBuffer.append(command[0:3])

def setPitch(pitch):
    command = []
    command += setPitchByte
    command += struct.pack('B',int(pitch+128))
    storage.dataBuffer.append(command[0:2])

def setDepthPidOn(depthPidIsOn):
    command = []
    command += setDepthPidOnByte
    command += struct.pack('b',int(depthPidIsOn))
    storage.dataBuffer.append(command[0:2])
    if (depthPidIsOn == 1):
        storage.depthPid = True
    else:
        storage.depthPid = False


def setPitchPidOn(pitchPidIsOn):
    command = []
    command += setPitchPidOnByte
    command += struct.pack('b',int(pitchPidIsOn))
    storage.dataBuffer.append(command[0:2])
    if (pitchPidIsOn == 1):
        storage.pitchPid = True
    else:
        storage.pitchPid = False

def calDepth():
    storage.dataBuffer.append(calDepthByte)

def getPitchRoll():
    storage.dataBuffer.append(getPitchRollByte)

def getDepth():
    storage.dataBuffer.append(getDepthByte)

def getThruster2():
    storage.dataBuffer.append(getThruster2Byte)

def getDepthPitchPid():
    storage.dataBuffer.append(getDepthPitchPidByte)
    
def setYaw(angle):
    command = []
    command += setYawByte
    command += struct.pack('h',int(angle))
    storage.dataBuffer.append(command[0:3])

def setYawPidOn(yawPidIsOn):
    command = []
    command += setYawPidOnByte
    command += struct.pack('b',int(yawPidIsOn))
    storage.dataBuffer.append(command[0:2])
    if (yawPidIsOn == 1):
        storage.yawPid = True
    else:
        storage.yawPid = False

def getYaw():
    storage.dataBuffer.append(getYawByte)

def getThruster4():
    storage.dataBuffer.append(getThruster4Byte)

def getYawValue():
    storage.dataBuffer.append(getYawValueByte)

def getPower():
    storage.dataBuffer.append(getPowerByte)

def setMag(magIsOn):
    command = []
    command += setMagByte
    command += struct.pack('b',int(magIsOn))
    storage.dataBuffer.append(command[0:2])
