from picamera.array import PiRGBArray
from picamera import PiCamera
import threading
import time
import detect
import cv2
import numpy as np
import sys

class piCamera_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__ (self)
        self.end = False

    def run(self):
        self.videoShow()

    def stop(self):
        self.end = True

    def videoShow(self):
        print("now in videoshow")
        camera = PiCamera()
        print("before rawcapture")
        camera.resolution = (640,480)
        camera.framerate = 10
        camera.shutter_speed = camera.exposure_speed
        camera.exposure_mode = 'off'
        rawCapture = PiRGBArray(camera)
        time.sleep(2)
        while (not self.end):
            print("inside loop")
            camera.capture(rawCapture, format="bgr")
            image = rawCapture.array
            cv2.imshow("raw", image)
    ##        print(detect.get_extreme_red_points(image))
    ##        print('a')

class webCamera_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__ (self)
        self._is_running = False
        self.end = False
        self.frame = None

    def showInfoEvent(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print ("x:",x)
            print ("y:",y)
            temp = self.frame[y][x]
            print (temp)
            print (cv2.cvtColor(np.uint8([[[temp[0],temp[1],temp[2]]]]), cv2.COLOR_BGR2HSV))

    def run(self):
##        cv2.namedWindow('frame')
##        cv2.setMouseCallback('frame', self.showInfoEvent)
##        self.videoCapture()
        self.videoShow()

    def stop(self):
        self.end = True

    def videoShow(self):
        print("now in videoshow")
        cap = cv2.VideoCapture(0)
        while(cap.isOpened() and not self.end):
            # Capture frame-by-frame
            ret, self.frame = cap.read()
            # Our operations on the frame come here
            # Display the resulting frame
            cv2.imshow('frame',self.frame)
            ###########################
            ###########################
            if cv2.waitKey(1) & 0xFF == ord('q'):
                 self.stop()
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    def videoCapture(self):
        cap = cv2.VideoCapture(0)
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

        while(cap.isOpened() and not self.end):
            ret, frame = cap.read()
            if ret==True:
##                cv2.imshow('frame',frame)
                frame = cv2.flip(frame,0)
                
                # write the flipped frame
                out.write(frame)
            else:
                break
        print("Cap end.......................")
        # Release everything if job is finished
        cap.release()
        out.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
#     camera = PiCamera()
#     camera.resolution = (640,480)
#     camera.framerate = 10
#     camera.shutter_speed = camera.exposure_speed
#     #camera.exposure_mode = 'off'
#     rawCapture = PiRGBArray(camera)
#     time.sleep(2)
#     while (True):
#         camera.capture(rawCapture, format="bgr")
#         image = rawCapture.array
#         cv2.imshow("raw", image)
# ##        print(detect.get_extreme_red_points(image))
# ##        print('a')
#         if cv2.waitKey(0) & 0xFF == ord('q'):
#             break
#         # clear the stream
# in preparation for the next frame
#         # if the `q` key was pressed, break from the loop
##    webCameraThread = webCamera_thread()
##    webCameraThread.daemon = True
##    webCameraThread.start()
    piCameraThread = piCamera_thread()
    piCameraThread.daemon = True
    piCameraThread.start()
    while True:
        if cv2.waitKey(0) & 0xFF == ord('q'):
##            webCameraThread.stop()
            piCameraThread.stop()
            print("now camera stop")
            break
##    webCameraThread.join()
    print("webcam join")
    piCameraThread.join()
    print("picam join")
    
    
