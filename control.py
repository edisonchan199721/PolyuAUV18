import struct
import threading
import storage
import controlApi as api
import time

class control_thread(threading.Thread):
    def __init__(self):
      threading.Thread.__init__ (self)

    def run(self):
       path()
       time.sleep(10)

def infoUpdate():
    api.calDepth()
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

def initialize():
    storage.initialize()
    infoUpdate()

def sink(depthSetPoint):
    api.calDepth()
    api.getDepth()
    api.setDepthPidOn(1)
    tempDepth = storage.depth
    for i in range(int(depthSetPoint/20)):
        api.setDepth(tempDepth+20)
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
    initialize()
    sink(20)
    terminate()
