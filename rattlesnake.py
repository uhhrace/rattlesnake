import pyautogui
import time
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
%matplotlib inline
import math
import cv2
from mss import mss

width, height = pyautogui.size()

def main():
	while(True):
		#do the thing
		time.sleep(3)
		detectEdges()
		turnAround()
		

def moveToCenter():
	pyautogui.moveTo(width / 2, height / 2)	
	
def turnAround():
	current_x, current_y = pyautogui.position()
	new_x = width - current_x
	new_y = height - current_y
	pyautogui.moveTo(new_x, new_y, 0);

def detectEdges():
	with mss() as sct:
		sct.shot()
		
	while "Screen capturing":
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = numpy.array(sct.grab(monitor))

        # Display the picture
        cv2.imshow("OpenCV/Numpy normal", img)

        # Display the picture in grayscale
        # cv2.imshow('OpenCV/Numpy grayscale',
        #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

        print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

	img = cv2.imread('messi5.jpg',0)
	edges = cv2.Canny(img,100,200)

	plt.subplot(121),plt.imshow(img,cmap = 'gray')
	plt.title('Original Image'), plt.xticks([]), plt.yticks([])
	plt.subplot(122),plt.imshow(edges,cmap = 'gray')
	plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

	plt.show()

	
main()