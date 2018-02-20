import struct
import threading
import storage
import controlApi as api
import time
import csv
import camera as camera
import sys

class control_thread(threading.Thread):
    def __init__(self):
      threading.Thread.__init__ (self)

    def run(self):
       path()
       #time.sleep(15)

def infoUpdate():
    api.getDepth()
    api.getYaw()
    api.getPitchRoll()
    api.getThruster2()
    api.getThruster4()
    api.getYawValue()

def terminate():
    api.move(0,0)
    api.setDepth(0)
    api.setDepthPidOn(0)
    api.setPitchPidOn(0)
    api.setYawPidOn(0)
    time.sleep(2)
    

def initialize():
    storage.reset()
    api.move(0,0)
    infoUpdate()
    api.calDepth()
    storage.initalYaw = storage.yaw
    storage.initalDepth = storage.depth
    storage.initalPitch = storage.pitch

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
    api.setYaw(storage.initalYaw)
    api.setYawPidOn(1)
    time.sleep(2)
    sink(30)
    api.setPitch(storage.initalPitch)
    api.setPitchPidOn(1)
    cameraThread = camera.camera_thread()
    cameraThread.daemon = True
    cameraThread.start()
    with open('data.csv', 'w') as csvfile:
        fieldnames = ['Time','Depth','Yaw','Pitch','Roll','Motor 0','Motor 1','Motor 2','Motor 3','Motor 4','Motor 5']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(150):
            time.sleep(0.2)
            infoUpdate()
            writer.writerow({'Time':int(i),'Depth':storage.depth,'Yaw':storage.yaw,'Pitch':storage.pitch,'Roll':storage.roll,'Motor 0':storage.motor[0],'Motor 1':storage.motor[1],'Motor 2':storage.motor[2],'Motor 3':storage.motor[3],'Motor 4':storage.motor[4],'Motor 5':storage.motor[5]})
    time.sleep(2)
    print('Termainate now')
    terminate()
