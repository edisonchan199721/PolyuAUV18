import time
import detect

def main():
    sleep(10)
    sink(depth/2)
    finished = False
    while(finished):
        finished = search_for_gate()
    movetogate()
    confirmgate()
    finished = False
    while(finished):
        finished = search_for_flare()
    movetoflare()
    floating()

def search_for_gate():
    while(True):
        if (checkDetected(1)):
            break
        yaw(left, 30)
        if (checkDetected(1)):
            break
        move(left, 5)
        if (checkDetected(1)):
            break
        yaw(right, 60)
        move(left, 10)
        if (checkDetected(1)):
            break
        #all checked, nothing detect, move forward to get a better sight
        yaw(left, 30)
        move(left, 5)
        move(forward, 2)
    # Its fucked if we cannot see the gate at all, so we dont care if we cant see it

def confirmgate():
    if green_angle < 0 and red_angle > 0:
        print ("Too Good to be True")
    move((green_angle+red_angle)/2,5)
    return True

def search_for_flare():
    while(True):
        if (checkDetected(2)):
            break
        yaw(left, 30)
        if (checkDetected(2)):
            break
        move(left, 5)
        if (checkDetected(2)):
            break
        yaw(right, 60)
        move(left, 10)
        if (checkDetected(2)):
            break
        #all checked, nothing detect, move forward to get a better sight
        yaw(left, 30)
        move(left, 5)
        move(forward, 3)

def checkDetected(color):
    return True if detect.getExPoints(color) else False

if __name__ == "__main__":
    main()
