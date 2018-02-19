import struct
import storage as storage

# Arduino no.0

setDepthByte = [0xA1] # short depth_setPoint [3 bytes]	(depth unit : cm)

setPitchByte = [0xA3]

setDepthPidOnByte = [0xAB]

calDepthByte = [0xAC]

setPitchPidOnByte = [0xAD]

getPitchRollBtye = [0xFA]

getThruster2Byte = [0xFB]

getDepthBtye = [0xFE]

# Arduino no.1

moveByte = [0xB1] # short angle + byte magnitude [4 bytes] (angle: From -180 to 180 degree , magnitude : 0 - 255)

setYawBtye = [0xB3]

setYawPidOnByte = [0xB7]

getYawByte = [0xFC]

getThruster4Byte = [0xFD]

getYawValueBtye = [0xFF]

sendToArduino0 = [0xA1,0xA3,0xAB,0xAC,0xAD,0xFA,0xFB,0xFE]
sendToArduino1 = [0xB1,0xB3,0xB7,0xFC,0xFD,0xFF]

def move(angle,magnitude):
    command = []
    command += moveByte
    command += struct.pack('h',int(angle))
    command += struct.pack('b',int(magnitude))
    storage.dataBuffer.append(command[0:4])

def setDepth(depth):
    command = []
    command += setDepthByte
    command += struct.pack('h',int(depth))
    storage.dataBuffer.append(command[0:3])

def setPitch(pitch):
    command = []
    command += setPitchByte
    command += struct.pack('b',int(pitch))
    storage.dataBuffer.append(command[0:2])

def setDepthPidOn(depthPidIsOn):
    command = []
    command += setDepthPidOnByte
    command += struct.pack('h',int(depthPidIsOn))
    storage.dataBuffer.append(command[0:2])

def setPitchPidOn(pitchPidIsOn):
    command = []
    command += setPitchPidOnByte
    command += struct.pack('h',int(pitchPidIsOn))
    storage.dataBuffer.append(command[0:2])

def calDepth():
    storage.dataBuffer.append(calDepthByte)

def getPitchRoll():
    storage.dataBuffer.append(getPitchRollBtye)
    storage.dataBuffer.append(getPitchRollBtye)

def getDepth():
    storage.dataBuffer.append(getDepthBtye)

def getThruster2():
    storage.dataBuffer.append(getThruster2Byte)

def setYaw(angle):
    command = []
    command += setYawByte
    command += struct.pack('h',int(angle))
    storage.dataBuffer.append(command[0:3])

def setYawPidOn(yawPidIsOn):
    command = []
    command += setYawPidOnByte
    command += struct.pack('h',int(yawPidIsOn))
    storage.dataBuffer.append(command[0:2])

def getYaw():
    storage.dataBuffer.append(getYawByte)

def getThruster4():
    storage.dataBuffer.append(getThruster4Byte)

def getYawValue():
    storage.dataBuffer.append(getYawValueBtye)
