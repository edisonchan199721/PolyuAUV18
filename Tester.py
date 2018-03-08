import time
import detect
import cv2
import numpy as np

frame = None

def showInfoEvent(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print ("x:", x)
        print ("y:", y)
        temp = frame[y][x]
        print (temp)
        print (cv2.cvtColor(np.uint8([[[temp[0], temp[1], temp[2]]]]), cv2.COLOR_BGR2HSV))


if __name__ == "__main__":
    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', showInfoEvent)
    cap = cv2.VideoCapture('output1002.avi')
    green_distance = detect.location()
    yellow_distance = detect.location()

    while (cap.isOpened()):
        cv2.waitKey(15)
        ret, frame = cap.read()

        yellow = detect.get_extreme_yellow_points(frame)
        green = detect.getExPoints(1, frame)
        if yellow:
            #print ("Y: ", yellow)
            for i, node in enumerate(yellow):
                if i < 2:
                    continue
                cv2.circle(frame, node, 10, (0, 255, 255), -1)
        if green:
            #print ("G: ", green)
            for i, node in enumerate(green):
                if i<2:
                    continue
                cv2.circle(frame, node, 10, (0, 255, 0), -1)
            a = green_distance.average_distance(detect.gate_location_calculation(None, green)[2][0])
            print (a, detect.gate_location_calculation(None, green)[2][1])

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
