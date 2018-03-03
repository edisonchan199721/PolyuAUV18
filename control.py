import struct
import threading
import storage
import controlApi as api
from datetime import datetime
import time
import csv
import camera as camera
import sys

class control_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__ (self)

    def run(self):
        time.sleep(1) #for setup waiting
        dryTest()
        terminate()

class dataLog_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__ (self)
        self.counter = 0
        self.end = False
        self.rate = 0.5

    def run(self):
        csvfile = open('data.csv', 'a')
        fieldnames = ['Time','Depth','Yaw','Pitch','Roll','Motor 0','Motor 1','Motor 2','Motor 3','Motor 4','Motor 5','Voltage','Current']
        writer = csv.writer(csvfile, delimiter=',',lineterminator='\n')
        writer.writerow([str(datetime.now().date()),str(datetime.now().time().strftime('%H:%M:%S'))])
        writer.writerow(fieldnames)
        csvfile.close()
        while not self.end:
            with open('data.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=',',lineterminator='\n')
                time.sleep(self.rate)
                writer.writerow([float("{0:.1f}".format(self.counter*self.rate)),storage.depth,storage.yaw,storage.pitch,storage.roll,storage.motor[0],storage.motor[1],storage.motor[2],storage.motor[3],storage.motor[4],storage.motor[5],storage.voltage,storage.current])
                infoUpdate()
                self.counter+=1

    def stop(self):
        self.end = True

def infoUpdate():
    api.getDepth()
    api.getYaw()
    api.getPitchRoll()
    api.getThruster2()
    api.getThruster4()
    api.getYawValue()
    api.getPower()

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
    tempDepth = storage.depth
    for i in range(int(depthSetPoint/sinkSpeed)):
        api.setDepth((i+1)*sinkSpeed)
        time.sleep(1)

# def stage0():
#
#
# def stage1():
#
# def stage2():
#
# def stage3():
#
# def stage4():

def path():
    initialize(True, True)
    dataLog = dataLog_thread()
    dataLog.daemon = True
    dataLog.start()
##    webCameraThread = camera.webCamera_thread()
##    webCameraThread.daemon = True
##    webCameraThread.start()
    time.sleep(2)
    sink(20,5)
    time.sleep(5)
##    api.move(0,120)
    time.sleep(10)
    print('Termainate now')
    dataLog.stop()
    dataLog.join()

def dryTest():
    time.sleep(10)
    storage.reset()
    dataLog = dataLog_thread()
    dataLog.daemon = True
    dataLog.start()
    initialize(True,True)
    time.sleep(20)
    api.setPitchPidOn(0)
    api.setYawPidOn(0)
    dataLog.stop()
    dataLog.join()

def directionTest():
    storage.reset()
    api.move(0,0)

def lightTest():
    storage.reset()
    api.setMag(1)
    time.sleep(60)
    api.setMag(0)

def test():
    storage.reset()
    initialize(True)
    dataLog = dataLog_thread()
    dataLog.daemon = True
    dataLog.start()
    ##############
##    api.move(0,60)
##    time.sleep(5)
##    api.move(180,60)
##    time.sleep(5)
    time.sleep(20)
    ###############
    dataLog.stop()
    dataLog.join()
