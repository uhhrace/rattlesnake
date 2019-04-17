import pyautogui
import time
import numpy as np
# import tensorflow as tf
import matplotlib.pyplot as plt
# from IPython import get_ipython
# get_ipython().run_line_magic('matplotlib', 'inline')
import math
import cv2
from mss import mss

width, height = pyautogui.size()


def main():
    while True:
        # Detect edges
        contours = detect_edges()

        # Find coordinates for biggest shape on screen
        cx, cy, c = find_biggest_thing(contours)

        # If biggest thing is bigger than a threshold, turn around
        if cv2.contourArea(c) > 3000:
            print("Snake size ", cv2.contourArea(c)," at ", cx, cy)
            # Move to biggest shape
            pyautogui.moveTo(cx, cy)
            turn_around()
        # Else, just go there
        else:
            pyautogui.moveTo(cx, cy)
            print("Snack size ", cv2.contourArea(c), " at ", cx, cy)


def find_biggest_thing(contours):
    c = max(contours, key=cv2.contourArea)

    M = cv2.moments(c)

    cx = int(M['m10'] / M['m00'])

    cy = int(M['m01'] / M['m00'])

    # If myself is the biggest object on screen, find next one
    if (cx + 20 == (width / 2) or cx - 20 == (width / 2) and
            cy + 20 == (height / 2) or cy - 20 == (height / 2)):
        print('Found self, finding another')
        contours.remove(c)
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

    return cx, cy, c


def move_circle():
    # move left side
    pyautogui.moveTo(100, height / 2, 10)
    # move bottom
    pyautogui.moveTo(width / 2, height - 100, 10)
    # move right side
    pyautogui.moveTo(width - 100, height / 2, 10)
    # move top
    pyautogui.moveTo(width / 2, 100, 10)


def move_to_center():
    pyautogui.moveTo(width / 2, height / 2)


def turn_around():
    current_x, current_y = pyautogui.position()
    new_x = width - current_x
    new_y = height - current_y
    pyautogui.moveTo(new_x, new_y, 0)


def detect_edges():
    with mss() as sct:
        monitor = {"top": 40, "left": 0, "width": width, "height": height}
        sct.shot()

        # last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = np.array(sct.grab(monitor))

        # Display the picture
        # cv2.imshow("OpenCV/Numpy normal", img)

        # Display the picture in grayscale
        # cv2.imshow('OpenCV/Numpy grayscale',
        #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

        # print("fps: {}".format(1 / (time.time() - last_time)))

        img = cv2.imread('monitor-1.png')
        edges = cv2.Canny(img, 100, 200)

        # Find the contours of the frame

        contours, hierarchy = cv2.findContours(edges.copy(), 1, cv2.CHAIN_APPROX_NONE)
        return contours

main()
