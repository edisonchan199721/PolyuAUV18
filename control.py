import struct
import threading
import storage
import controlApi as api
from datetime import datetime
import time
import csv
import camera as camera
import sys
import detect

class control_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__ (self)

    def run(self):
        time.sleep(1) #for setup waiting
        dataLog = dataLog_thread()
        dataLog.daemon = True
        dataLog.start()
        webCameraThread = camera.webCamera_thread()
        webCameraThread.daemon = True
        webCameraThread.start()
        time.sleep(20) # For dry test
        if(storage.stage[0]):
            qualificationControl()
            storage.stage[0] = False
        if(storage.stage[1]):
            stage1Control()
            storage.stage[1] = False
        terminate()
        webCameraThread.stop()
        webCameraThread.join()
        print("web cam join")
        dataLog.stop()
        dataLog.join()
        print("datalog join")


class dataLog_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__ (self)
        self.counter = 0
        self.end = False
        self.rate = 1

    def run(self):
        csvfile = open('data.csv', 'a')
        fieldnames = ['Time','Depth','Yaw','Pitch','Roll','Motor 0','Motor 1','Motor 2','Motor 3','Motor 4','Motor 5','Voltage','Current','depth_Kp', 'depth_Ki', 'depth_Kd', 'pitch_Kp', 'pitch_Ki', 'pitch_Kd','depth_Pid','yaw_Pid','pitch_Pid']
        writer = csv.writer(csvfile, delimiter=',',lineterminator='\n')
        writer.writerow([str(datetime.now().date()),str(datetime.now().time().strftime('%H:%M:%S'))])
        writer.writerow(fieldnames)
        csvfile.close()
        while not self.end:
            with open('data.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=',',lineterminator='\n')
                time.sleep(self.rate)
                writer.writerow([float("{0:.1f}".format(self.counter*self.rate)),storage.depth,storage.yaw,storage.pitch,storage.roll,storage.motor[0],storage.motor[1],storage.motor[2],storage.motor[3],storage.motor[4],storage.motor[5],storage.voltage,storage.current,storage.depth_Kp,storage.depth_Ki,storage.depth_Kd,storage.pitch_Kp,storage.pitch_Ki,storage.pitch_Kd,storage.depthPid,storage.yawPid,storage.pitchPid])
                infoUpdate()
                self.counter+=1

    def stop(self):
        self.end = True

def infoUpdate():
    api.getDepth()
    api.getYaw()
    api.getPitchRoll()
    ## Image info update
    storage.yellowObject = detect.getExPoints(2, storage.webCameraImage)
    storage.greenObject = detect.getExPoints(1, storage.webCameraImage)
    storage.redObject = detect.getExPoints(0, storage.webCameraImage)
    if(storage.greenObject):
        storage.greenObjectInfo=[self.green_distance.average_distance(detect.gate_location_calculation(None, storage.greenObject)[2][0]),detect.gate_location_calculation(None, storage.greenObject)[2][1]]
    else:
        storage.greenObjectInfo = []
    if(storage.yellowObject):
        storage.yellowObjectInfo=[self.yellow_distance.average_distance(detect.gate_location_calculation(None, storage.yellowObject)[2][0]),detect.gate_location_calculation(None, storage.yellowObject)[2][1]]
    else:
        storage.yellowObjectInfo = []
    if(storage.redObject):
        storage.redObjectInfo=[self.red_distance.average_distance(detect.gate_location_calculation(None, storage.redObject)[2][0]),detect.gate_location_calculation(None, storage.redObject)[2][1]]
    else:
        storage.redObjectInfo = []
    print("Green Distance:",storage.greenObjectInfo[0],"Green Angle:",storage.greenObjectInfo[1])
    print("Yellow Distance:",storage.greenObjectInfo[0],"Yellow Angle:",storage.greenObjectInfo[1])
    print("Red Distance:",storage.greenObjectInfo[0],"Red Angle:",storage.greenObjectInfo[1])
##    api.getThruster2()
##    api.getThruster4()
##    api.getYawValue()
##    api.getPower()
##    api.getDepthPitchPid()

def terminate():
    api.move(0,0)
    api.setDepth(0)
    api.setDepthPidOn(0)
    api.setPitchPidOn(0)
    api.setYawPidOn(0)
    storage.end = True
    api.move(0,0)
    print('Termainate now')

def initialize(YawPidOn=False,PitchPidOn=False):
    print('Initialize now')
    storage.reset()
    api.move(0,0)
    api.calDepth()
    infoUpdate()
    api.setDepthPid(7,0,0)
    api.setPitchPid(6,0.75,120)
    storage.initialVariable()
    time.sleep(1)
    if (YawPidOn):
        api.setYaw(storage.initialYaw)
        api.setYawPidOn(1)
    if (PitchPidOn):
        api.setPitch(storage.initialPitch)
        api.setPitchPidOn(1)

def sink(depthSetPoint,sinkSpeed=10): #sinkSpeed is the sinking distance(cm) per second, usually 10 or 5.
    api.getDepth()
    api.setDepthPidOn(1)
    for i in range(int(depthSetPoint/sinkSpeed)):
        api.setDepth((i+1)*sinkSpeed)
        time.sleep(1)
    while not (storage.depth >= (depthSetPoint-10) and storage.depth <= (depthSetPoint+10))
        time.sleep(1)

def setYaw(yawSetPoint):
    api.setYaw(yawSetPoint)
    while not (storage.yaw >= (yawSetPoint-2) and storage.yaw <= (yawSetPoint+2)):
        time.sleep(1)

def stage1Control():
    sink(100,5)
    while not (storage.greenObject):
        searchGreenObject()

# def stage2Control():
#
# def stage3Control():
#
def stage4Control():



def searchGreenObject():
    api.move(0,0)
    if(storage.greenObject):
        return
    for i in range(3):
        setYaw(storage.initialYaw-((i+1)*20))
        time.sleep(2)
        if(storage.greenObject):
            return
    for i in range(3):
        setYaw(storage.initialYaw+((i+1)*20))
        time.sleep(2)
        if(storage.greenObject):
            return
    setYaw(storage.initialYaw)
    time.sleep(2)
    api.move(0,100)
    time.sleep(5)


def lightTest():
    storage.reset()
    api.setMag(1)
    time.sleep(60)
    api.setMag(0)

def qualificationControl():
    initialize(True,True)
    sink(100,5)
    move(0,200)
    time.sleep(20)
