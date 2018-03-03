from picamera.array import PiRGBArray
from picamera import PiCamera
import threading
import time
import detect
import cv2

class piCamera_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__ (self)
        self.end = False

    def run(self):
        self.videoShow()

    def stop(self):
        self.end = True

    def videoShow(self):
        camera = PiCamera()
        camera.resolution = (640,480)
        camera.framerate = 10
        camera.shutter_speed = camera.exposure_speed
        camera.exposure_mode = 'off'
        rawCapture = PiRGBArray(camera)
        time.sleep(2)
        while (not self.end):
            camera.capture(rawCapture, format="bgr")
            image = rawCapture.array
            cv2.imshow("raw", image)
            ###########################

            ###########################
    ##        print(detect.get_extreme_red_points(image))
    ##        print('a')

class webCamera_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__ (self)
        self._is_running = False
        self.end = False

    def run(self):
        print("Hi")
        self.videoCapture()
        #self.videoShow()

    def stop(self):
        self.end = True

    def showInfoEvent(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print ("x:",x)
            print ("y:",x)

    def videoShow(self):
        cap = cv2.VideoCapture(0)
        while(cap.isOpened() and not self.end):
            # Capture frame-by-frame
            ret, frame = cap.read()
            # Our operations on the frame come here
            # Display the resulting frame
            cv2.imshow('frame',frame)
            cv2.setMouseCallback('frame', showInfoEvent)
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

        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret==True:
                frame = cv2.flip(frame,0)

                # write the flipped frame
                out.write(frame)

                cv2.imshow('frame',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

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
#         # clear the stream in preparation for the next frame
#         # if the `q` key was pressed, break from the loop
    webCameraThread = webCamera_thread()
    webCameraThread.daemon = True
    webCameraThread.start()
    time.sleep(20)
    
