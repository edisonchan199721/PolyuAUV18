# import the necessary packages
import math
import cv2
import numpy as np

def get_extreme_red_points(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #common grey
    lower_grey = np.array([0, 0, 100])
    upper_grey = np.array([180, 20, 200])

    # red
    lower_red = np.array([0, 25, 110])
    upper_red = np.array([15, 55, 200])
    lower_red1 = np.array([150, 25, 110])
    upper_red1 = np.array([180, 55, 200])

    # mask
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_red += cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red += cv2.inRange(hsv, lower_grey, upper_grey)

    extreme_points_red = None

    ##_red contour
    image_red, contours_red, hierarchy_red = cv2.findContours(mask_red, cv2.RETR_EXTERNAL,
                                                              cv2.CHAIN_APPROX_NONE)  # cv2.CHAIN_APPROX_SIMPLE
    contours_red = sorted(contours_red, key=cv2.contourArea)
    c = None
    while True:
        if len(contours_red) == 0:
            break
        cx = contours_red[-1]
        if cv2.contourArea(cx) < 300 or cv2.contourArea(cx) > 3500 :
            break
        (x, y), (MA, ma), angle = cv2.fitEllipse(cx)
        if (not ((angle < 30) or (angle > 120))) or (cv2.arcLength(cx, True) < 180):
            del contours_red[-1]
        else:
            c = cx
            break
    # LRTB
    try:
        extreme_points_red = [tuple(c[c[:, :, 0].argmin()][0]), tuple(c[c[:, :, 0].argmax()][0]),
                              tuple(c[c[:, :, 1].argmin()][0]), tuple(c[c[:, :, 1].argmax()][0])]
    except:
        pass
        #print ('No red')

    return extreme_points_red


def get_extreme_green_points(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #common grey
    lower_grey = np.array([0, 0, 100])
    upper_grey = np.array([180, 20, 200])

    # green
    lower_green = np.array([75, 153, 145])
    upper_green = np.array([96, 230, 192])
    # mask
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    #mask_green += cv2.inRange(hsv, lower_grey, upper_grey)

    extreme_points_green = None

    ##_green contour
    image_green, contours_green, hierarchy_green = cv2.findContours(mask_green, cv2.RETR_EXTERNAL,
                                                                    cv2.CHAIN_APPROX_NONE)  # cv2.CHAIN_APPROX_SIMPLE
    contours_green = sorted(contours_green, key=cv2.contourArea)
    c = None
    while True:
        # Break when no more contour to consider
        # aka nothing good detected
        if len(contours_green) == 0:
            break
        # last one is the largest contour
        cx = contours_green[-1]
        # Remining contour to small to be significant
        if cv2.contourArea(cx) < 300 or cv2.contourArea(cx) > 3500 :
            break
        # Get angle of the contour, prevent capturing the bottom green band
        # Or considering distant objects as blacks
        (x, y), (MA, ma), angle = cv2.fitEllipse(cx)
        if (not ((angle < 30) or (angle > 120))) or (cv2.arcLength(cx, True) < 180):
            del contours_green[-1]
        else:
            print cv2.arcLength(cx, False), " + ", cv2.contourArea(cx)
            c = cx
            break
    # LRTB
    try:
        extreme_points_green = [tuple(c[c[:, :, 0].argmin()][0]), tuple(c[c[:, :, 0].argmax()][0])
            , tuple(c[c[:, :, 1].argmin()][0]), tuple(c[c[:, :, 1].argmax()][0])]
    except:
        pass
        #print ('No green')

    return extreme_points_green

def get_extreme_yellow_points(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # yellow
    lower_yellow = np.array([75, 90, 100])
    upper_yellow = np.array([90, 180, 166])


    # mask
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    extreme_points_yellow = None

    ##_green contour
    image_yellow, contours_yellow, hierarchy_yellow = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL,
                                                                    cv2.CHAIN_APPROX_NONE)  # cv2.CHAIN_APPROX_SIMPLE
    contours_yellow = sorted(contours_yellow, key=cv2.contourArea)
    c = None
    while True:
        # Break when no more contour to consider
        # aka nothing good detected
        if len(contours_yellow) == 0:
            break
        # last one is the largest contour
        cx = contours_yellow[-1]
        # Remining contour to small to be significant
        if cv2.contourArea(cx) < 300 or cv2.contourArea(cx) > 3500 :
            break
        # Get angle of the contour, prevent capturing the bottom green band
        # Or considering distant objects as blacks
        (x, y), (MA, ma), angle = cv2.fitEllipse(cx)

# or (cv2.arcLength(cx, True)/cv2.contourArea(cx) < 2.0)
        if (not ((angle < 30) or (angle > 120))) or (cv2.arcLength(cx, True) < 180):
            del contours_yellow[-1]
        else:
            c = cx
            print cv2.arcLength(cx, False), " + ", cv2.contourArea(cx)
            break
    # LRTB
    try:
        extreme_points_yellow = [tuple(c[c[:, :, 0].argmin()][0]), tuple(c[c[:, :, 0].argmax()][0])
            , tuple(c[c[:, :, 1].argmin()][0]), tuple(c[c[:, :, 1].argmax()][0])]
    except:
        pass
        #print ('No yellow')

    return extreme_points_yellow

def gate_location_calculation(extreme_points_red, extreme_points_green):
    # Return None if no yellow detected, else return (DistanceToYellow, AngleToYellow)
    red_angle, green_angle, red_distance, green_distance = None, None, None, None
    if extreme_points_red is not None:
        red_distance = int(math.sqrt((extreme_points_red[2][0]-extreme_points_red[3][0])**2+(extreme_points_red[2][1]-extreme_points_red[3][1])**2))
        red_distance = 100/red_distance # or what ever measured real pixel at 1 m
        #assume 100 pixels at 1m, 10 pixels mean same object at 10m
        red_mid_point = int((extreme_points_yellow[2][0]+extreme_points_yellow[3][0])/2)
        if red_mid_point <= 640:
            red_mid_point = 640 - red_mid_point
        else:
            red_mid_point = red_mid_point - 640
        red_angle = int(red_mid_point/640*60)
    if extreme_points_green is not None:
        green_distance = int(math.sqrt((extreme_points_green[2][0]-extreme_points_green[3][0])**2+(extreme_points_green[2][1]-extreme_points_green[3][1])**2))
        green_distance = 100/green_distance # or what ever measured real pixel at 1 m
        #assume 100 pixels at 1m, 10 pixels mean same object at 10m
        green_mid_point = int((extreme_points_green[2][0]+extreme_points_green[3][0])/2)
        if green_mid_point <= 640:
            green_mid_point = 640 - green_mid_point
        else:
            green_mid_point = green_mid_point - 640
        green_angle = int(green_mid_point/640*60)
    deviation = None
    if (red_angle is not None) and (green_angle is not None):
        deviation = (abs(red_angle-green_angle)>20) and (red_distance > 2) and (green_distance > 2)
        deviation = deviation or (abs(red_distance-green_distance)>2)
    return deviation, (red_distance, red_angle) , (green_distance, green_angle)

def flare_location_calculation(extreme_points_yellow):
    # Return None if no yellow detected, else return (DistanceToYellow, AngleToYellow)
    if extreme_points_yellow is not None:
        yellow_distance = int(math.sqrt((extreme_points_yellow[2][0]-extreme_points_yellow[3][0])**2+(extreme_points_yellow[2][1]-extreme_points_yellow[3][1])**2))
        yellow_distance = 100/yellow_distance # or what ever measured real pixel at 1 m
        #assume 100 pixels at 1m, 10 pixels mean same object at 10m
        yellow_mid_point = int((extreme_points_yellow[2][0]+extreme_points_yellow[3][0])/2)#, int((extreme_points_yellow[2][1]+extreme_points_yellow[3][1])/2))
        if yellow_mid_point <= 640:
            yellow_mid_point = 640 - yellow_mid_point
        else:
            yellow_mid_point = yellow_mid_point - 640
        return yellow_distance, int(yellow_mid_point/640*60)
    return None

if __name__ == "__main__":
    frame = cv2.imread('test1.5m2.jpg')
    frame = cv2.imread('test12_cr.jpg')
    gate_location_calculation(get_extreme_red_points(frame))