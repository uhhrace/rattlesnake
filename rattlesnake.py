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
        # do the thing
        # Wait three sec
        time.sleep(3)
        # detect edges
        detect_edges()
        # decide if we want to turn around
        #turn_around()
        #move_circle()
        #pyautogui.moveTo(width / 2, height / 2 - 125)
        #pyautogui.click()


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
    pyautogui.moveTo(new_x, new_y, 10)


def detect_edges():
    with mss() as sct:
        monitor = {"top": 40, "left": 0, "width": width, "height": height}
        sct.shot()

        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = np.array(sct.grab(monitor))

        # Display the picture
        # cv2.imshow("OpenCV/Numpy normal", img)

        # Display the picture in grayscale
        # cv2.imshow('OpenCV/Numpy grayscale',
        #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

        print("fps: {}".format(1 / (time.time() - last_time)))

        img = cv2.imread('monitor-1.png')
        edges = cv2.Canny(img, 100, 200)

        plt.subplot(121), plt.imshow(img, cmap='gray')
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(edges, cmap='gray')
        plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

        plt.show()
        current_x, current_y = pyautogui.position()

        currentXRange = []
        currentYRange = []
'''
        # If mouse in left side of screen
        if current_x < width / 2:
            # Fill array with values from 0 to mouse position
            for x in range(0, current_x):
                currentXRange[x] = x
        # If mouse in right side of screen
        else:
            # Fill array with values from position to edge of screen
            for x in range(current_x, width):
                currentXRange[x - current_x] = x

        # If mouse in top half of screen
        if current_y < height/ 2:
            # Fill array with values from 0 to mouse position
            for y in range(0, current_y):
                currentYRange[y] = y
        # If mouse in bottom half of screen
        else:
            # Fill array with values from mouse position to bottom of screen
            for y in range(current_y, width):
                currentYRange[y - current_y] = y

        plt.plot(currentXRange, currentYRange, linewidth=20.0)
'''

main()
