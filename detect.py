# import the necessary packages
import math
import cv2
import numpy as np

class location():
    def __init__(self):
        self.distance_list = []
        self.smaller, self.larger = [],[]

    def average_distance(self, distance):
        self.distance_list.append(distance)
        if len(self.distance_list) > 25:
            self.distance_list.pop(0)
        if all(v is None for v in self.distance_list):
            return None
        temp = [x for x in self.distance_list if x is not None]
        average = sum(temp)/len(temp)
        for node in temp:
            if average > node:
                self.smaller.append(node)
            else:
                self.larger.append(node)
        temp = self.larger if len(self.larger)>len(self.smaller) else self.smaller
        return sum(temp) / len(temp)

def getExPoints(color, image, show = False):
    # 0 = Red, 1 = Green, 2 = yellow
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # red
    lower_red = np.array([0, 25, 110])
    upper_red = np.array([15, 55, 200])
    lower_red1 = np.array([150, 25, 110])
    upper_red1 = np.array([180, 55, 200])
    # yellow
    lower_yellow = np.array([75, 90, 100])
    upper_yellow = np.array([95, 185, 166])
    # green
    lower_green = np.array([75, 153, 145])
    upper_green = np.array([96, 238, 192])

    # mask
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_red += cv2.inRange(hsv, lower_red1, upper_red1)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    extreme_points = None

    image, contours, hierarchy = cv2.findContours((mask_red if color == 0 else mask_green if color == 1 else mask_yellow), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)  # cv2.CHAIN_APPROX_SIMPLE
    contours = sorted(contours, key=cv2.contourArea)
    c = None
    while True:
        if len(contours) == 0:
            break
        cx = contours[-1]
        if cv2.contourArea(cx) < 300 or cv2.contourArea(cx) > 3500 :
            break
        (x, y), (MA, ma), angle = cv2.fitEllipse(cx)
        if (not ((angle < 30) or (angle > 120))) or (cv2.arcLength(cx, True) < 180):
            del contours[-1]
        else:
            c = cx
            break
    # LRTB
    try:
        extreme_points = [tuple(c[c[:, :, 0].argmin()][0]), tuple(c[c[:, :, 0].argmax()][0]),
                          tuple(c[c[:, :, 1].argmin()][0]), tuple(c[c[:, :, 1].argmax()][0])]
    except:
        if show:
            print ("No such color detected : ",color)
        else:
            pass

    return extreme_points

def gate_location_calculation(extreme_points_red, extreme_points_green):
    # Return None if no yellow detected, else return (DistanceToYellow, AngleToYellow)
    red_angle, green_angle, red_distance, green_distance = 0.0, 0.0, 0.0, 0.0
    if extreme_points_red is not None:
        red_distance = math.sqrt((extreme_points_red[2][0]-extreme_points_red[3][0])**2+(extreme_points_red[2][1]-extreme_points_red[3][1])**2)
        red_distance = 222*9/red_distance # or what ever measured real pixel at 1 m
        #assume 100 pixels at 1m, 10 pixels mean same object at 10m
        red_mid_point = (extreme_points_red[2][0]+extreme_points_red[3][0])/2 -320
        red_angle = float(red_mid_point)/640*60
    if extreme_points_green is not None:
        green_distance = math.sqrt((extreme_points_green[2][0]-extreme_points_green[3][0])**2+(extreme_points_green[2][1]-extreme_points_green[3][1])**2)
        green_distance = 222*9/green_distance # or what ever measured real pixel at 1 m
        #assume 100 pixels at 1m, 10 pixels mean same object at 10m
        green_mid_point = (extreme_points_green[2][0]+extreme_points_green[3][0])/2 - 320
        green_angle = green_mid_point/640*60
    deviation = None
    if (red_angle is not None) and (green_angle is not None):
        deviation = (abs(red_angle-green_angle)>20) and (red_distance > 2) and (green_distance > 2)
        deviation = deviation or (abs(red_distance-green_distance)>2)
    return deviation, (red_distance, red_angle) , (green_distance, green_angle)

def flare_location_calculation(extreme_points_yellow):
    # Return None if no yellow detected, else return (DistanceToYellow, AngleToYellow)
    if extreme_points_yellow is not None:
        yellow_distance = int(math.sqrt((extreme_points_yellow[2][0]-extreme_points_yellow[3][0])**2+(extreme_points_yellow[2][1]-extreme_points_yellow[3][1])**2))
        yellow_distance = 222*9/yellow_distance # or what ever measured real pixel at 1 m
        #assume 100 pixels at 1m, 10 pixels mean same object at 10m
        yellow_mid_point = int((extreme_points_yellow[2][0]+extreme_points_yellow[3][0])/2) - 320
        return yellow_distance, int(yellow_mid_point/640*60)
    return None

if __name__ == "__main__":
    frame = cv2.imread('test1.5m2.jpg')
    frame = cv2.imread('test12_cr.jpg')
    gate_location_calculation(get_extreme_red_points(frame))
