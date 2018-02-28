import struct
import serial
import threading
import time
import controlApi as controlApi
import control as control
import storage as storage
import sys

# for serial mapping
serialMap = [serial.Serial(),serial.Serial(),serial.Serial(),serial.Serial()]
serialStatus = [False,False,False,False]
serialName = ['','','','']

# return corresponding serial number
def serialNumber(detail):
   if detail == 0xA1:
      return 0
   elif detail == 0xB1:
      return 1
   elif detail == 0xC1:
      return 2
   elif detail == 0xD1:
      return 3
   return -1

# reconnect serial port
def serialReconnect(portName):
   ser = None
   while 1:
      try:
         ser = serial.Serial(portName,115200)
         break
      except serial.serialutil.SerialException:
         print("Serial unable to reconnect.")
         time.sleep(5)
         pass
   return ser

# disable the duplicate port when reconnecting
def serialDisable(sNum,portName):
   if(sNum == -1): return
   for i in range(4):
      if(i != sNum and serialName[i] == serialName[sNum]):
         serialStatus[i] = False
         serialMap[i] = None #have to check if serial.Serial() or None is better
         serialName[i] = portName

# Send command to corresponding arduino
def send():
    writeTo = -1
    while not (len(storage.dataBuffer)==0):
        try:
            if(storage.dataBuffer[0][0] in controlApi.sendToArduino0):
                writeTo = 0
                serialMap[writeTo].write(bytes(storage.dataBuffer[0]))
            elif(storage.dataBuffer[0][0] in controlApi.sendToArduino1):
                writeTo = 1
                serialMap[writeTo].write(bytes(storage.dataBuffer[0]))
            elif(storage.dataBuffer[0][0] in controlApi.sendToArduino2):
                writeTo = 2
                serialMap[writeTo].write(bytes(storage.dataBuffer[0]))
                print("Write to arduino 2")
            if(storage.dataBuffer[0][0] >= 192):
                receive(writeTo)
            else:
                del storage.dataBuffer[0]
        except serial.serialutil.SerialException:
            if (writeTo != -1):
                print("Serial ",writeTo," Port:",server.serialName[writeTo]," is disconnected")
                server.serialStatus[writeTo] = False
                serialTemp = server.serialReconnect(serialName[writeTo])
                serialTemp.write(command)

# Receive data from corresponding arduino
def receive(receivedFrom):
    # Serial Read loop
    received = False
    serialTemp = serialMap[receivedFrom] # Temp for current Arduino
    while not (received):
        try:
           otherPort = -1
           otherPortName = ''
           if(serialTemp.inWaiting() >= 2):
              info = serialTemp.read(1)
              if info[0] == 0xF2:
                 detail = serialTemp.read(1)
                 sNum = serialNumber(detail[0])
                 if(sNum == -1):
                    print("Connected Arduino does not match the system / Return Data Error, data:",detail[0])
                 else:
                    serialMap[sNum] = serialTemp
                    # if different from orignal port, record and erase another one by serialDisable Function
                    if(serialName[sNum] != serialMap[sNum].port):
                       otherPort = sNum
                       otherPortName = serialName[sNum]
                    serialName[sNum] = serialMap[sNum].port
                    if(not serialStatus[sNum]):
                       print("Serial No:",sNum+1," Port:",serialMap[sNum].port,"is online")
                    serialStatus[sNum] = True
              elif info[0] == 0xE2: # Arduino 1
                 storage.pitch = struct.unpack('h',serialTemp.read(2))[0]
                 storage.roll = struct.unpack('h',serialTemp.read(2))[0]
                 print('Pitch:',storage.pitch,'Roll:', storage.roll)
                 received = True
              elif info[0] == 0xE3: # Arduino 1
                 storage.motor[0] = struct.unpack('h',serialTemp.read(2))[0]
                 storage.motor[1] = struct.unpack('h',serialTemp.read(2))[0]
                 storage.motorValue[0] = True
                 print('Motor 0:',storage.motor[0],'Motor 1:', storage.motor[1])
                 received = True
              elif info[0] == 0xE4: # Arduino 2
                 storage.yaw = struct.unpack('h',serialTemp.read(2))[0]
                 print('Yaw:',storage.yaw)
                 received = True
              elif info[0] == 0xE5: # Arduino 2
                 storage.motor[2] = struct.unpack('h',serialTemp.read(2))[0]
                 storage.motor[3] = struct.unpack('h',serialTemp.read(2))[0]
                 storage.motor[4] = struct.unpack('h',serialTemp.read(2))[0]
                 storage.motor[5] = struct.unpack('h',serialTemp.read(2))[0]
                 storage.motorValue[1] = True
                 print('Motor 2:',storage.motor[2],'Motor 3:',storage.motor[3],'Motor 4:',storage.motor[4],'Motor 5:',storage.motor[5])
                 received = True
              elif info[0] == 0xE6: # Arduino 1
                 storage.depth = struct.unpack('h',serialTemp.read(2))[0]
                 print('depth:',storage.depth)
                 received = True
              elif info[0] == 0xE7: # Arduino 1
                 storage.yawSetPoint = struct.unpack('h',serialTemp.read(2))[0]
                 print('Yaw set point:',storage.yawSetPoint)
                 received = True
             elif info[0] == 0xEA:
                 storage.voltage = float("{0:.2f}".format(struct.unpack('f',serialTemp.read(4))[0])
                 storage.current = float("{0:.2f}".format(struct.unpack('f',serialTemp.read(4))[0])
                 print('Voltage:',storage.voltage,'Current:',storage.current)
                 received = True
        except serial.serialutil.SerialException:
            print("Serial Error Occur, Port: ",writeTo)
            serialTemp = serialReconnect(serialName[writeTo])
            serialTemp.write(command)
        serialDisable(otherPort,otherPortName)
        if(received):
            serialTemp.read(serialTemp.inWaiting())
            del storage.dataBuffer[0]
            break
##        elif((serialTemp.inWaiting() <= 2) and not received):
##            time.sleep(0.2)
##            break
##        elseif((serialTemp.inWaiting() <= 2) and received):
##            serialTemp.read(serialTemp.inWaiting())
##            del storage.dataBuffer[0]
##            break
      # check serial status

class server_thread(threading.Thread):
   def __init__(self):
      threading.Thread.__init__ (self)

   def run(self):
       while not storage.end:
           while not(len(storage.dataBuffer)==0):
               send()

########################### Main ############################
if __name__ == "__main__":
   #----------------------------Serial Port Setup
   # init serial variable
   serialNo = [serial.Serial(),serial.Serial(),serial.Serial(),serial.Serial()]

   # init serial port
   command = bytearray([0xF1]) # command for get arduino type
   serialNo[0] = serialReconnect('/dev/ttyUSB0')
   serialNo[1] = serialReconnect('/dev/ttyUSB1')
   serialNo[2] = serialReconnect('/dev/ttyUSB2')
   # serialNo[3] = serialReconnect('/dev/ttyUSB3')
   # serial mapping before main loop
   for i in range(3):
      serialNo[i].read(serialNo[i].inWaiting())
   while True:
      # for serial mapping
      serialNo[0].write(command)
      serialNo[1].write(command)
      serialNo[2].write(command)
      # serialNo[3].write(command)
      for i in range(3):
         try:
##            if(serialMapped[i]):
##               continue
##            else serialNo[i].write(command)
            print(i,':',serialNo[i].inWaiting())
            if(serialNo[i].inWaiting() >= 2):
               info = serialNo[i].read(1)
               if info[0] == 0xF2:
                  detail = serialNo[i].read(1)
                  sNum = serialNumber(detail[0])
                  if(sNum == -1):
                     print("Connected Arduino does not match the system / Return Data Error, data:",detail[0])
                  else:
                     serialMap[sNum] = serialNo[i]
                     if(not serialStatus[sNum]):
                        print("Serial No:",sNum+1," Port:",serialMap[sNum].port,"is online")
                     serialStatus[sNum] = True
##                     serialMapped[i] = True
                     serialName[sNum] = serialMap[sNum].port
               elif info[0] == 0xE1: # if go up data on Arduino3 appear first
                  detail = serialNo[i].read(7)
                  info += detail
                  serialMap[2] = serialNo[i]
                  if(not serialStatus[2]):
                     print("Serial No: 3 Port:",serialMap[2].port,"is online")
                  serialStatus[2] = True
##                  serialMapped[i] = True
                  serialName[2] = serialMap[2].port
                  # try to write to client
         except serial.serialutil.SerialException:
            print("Serial Error Occur, Port: ",i)
            name = '/dev/ttyUSB'+str(i)
            serialNo[i] = serialReconnect(name)
      print(serialStatus[0],serialStatus[1],serialStatus[2],serialStatus[3])
      time.sleep(0.5)
      #if(serialStatus[0] and serialStatus[1] and serialStatus[2] and serialStatus[3]):
      if(serialStatus[0] and serialStatus[1] and serialStatus[2]):
         print('All Arduino is ready')
         break

   # Control Thread setup
   control = control.control_thread()
   control.daemon = True
   control.start()
   # Server Thread setup
   server = server_thread()
   server.daemon = True
   server.start()

   control.join()
   print("Control join")
   server.join()
   print("Server join")
   sys.exit()
   # Camera Thread setup
   # camera = camera.control_thread()
   # camera.daemon = True
   # camera.start()
