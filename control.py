import struct
import threading
import storage
import controlApi as api
from datetime import datetime
import time
import csv
# import camera as camera
import sys

class control_thread(threading.Thread):
    def __init__(self):
      threading.Thread.__init__ (self)

    def run(self):
       dryTest()
       #time.sleep(15)

class dataLog_thread(threading.Thread):
    def __init__(self):
      threading.Thread.__init__ (self)
      self.counter = 0
      self.end = False
      self.rate = 1

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

def initialize():
    print('Initialize now')
    storage.reset()
    api.move(0,0)
    api.calDepth()
    infoUpdate()
    storage.initialVariable()
    api.setYaw(storage.initialYaw)
    api.setYawPidOn(1)
    api.setPitch(storage.initialPitch)
    api.setPitchPidOn(1)

def sink(depthSetPoint):
    api.getDepth()
    api.setDepthPidOn(1)
    tempDepth = storage.depth
    for i in range(int(depthSetPoint/5)):
        api.setDepth((i+1)*5)
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
    time.sleep(30)
    initialize()
    dataLog = dataLog_thread()
    dataLog.daemon = True
    dataLog.start()
    time.sleep(2)
    sink(30)
    # cameraThread = camera.camera_thread()
    # cameraThread.daemon = True
    # cameraThread.start()
    time.sleep(2)
    print('Termainate now')
    terminate()
    dataLog.stop()
    dataLog.join()

def dryTest():
    storage.reset()
    dataLog = dataLog_thread()
    dataLog.daemon = True
    dataLog.start()
    time.sleep(10)
    print('Termainate now')
    terminate()
    dataLog.stop()
    dataLog.join()

def directionTest():
    storage.reset()
    api.move(0,0)
    terminate()
