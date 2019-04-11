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
        # Wait one sec
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
    pyautogui.moveTo(new_x, new_y, 10);


def detect_edges():
    with mss() as sct:
        monitor = {"top": 40, "left": 0, "width": width, "height": height}
        sct.shot()

        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = np.array(sct.grab(monitor))

        # Display the picture
        cv2.imshow("OpenCV/Numpy normal", img)

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
        time.sleep(1)
        cv2.destroyAllWindows()

main()