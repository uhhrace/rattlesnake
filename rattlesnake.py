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
import webbrowser
'''
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
'''

# Record size : 1491

width, height = pyautogui.size()


def main():
    # webbrowser.open('http://slither.io/')
    chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    webbrowser.get('chrome').open_new_tab('http://slither.io/')
    time.sleep(5)
    start_game()
    while True:
        start_game()
        # alpha_protocol()
        # beta_protocol()
        gamma_protocol()
        print('Game over man')


def start_game():

    contours = detect_edges()
    cx, cy, c = find_biggest_thing(contours)
    pyautogui.moveTo(cx, cy + 100)
    pyautogui.click()


def find_biggest_thing(contours):
    c = max(contours, key=cv2.contourArea)

    M = cv2.moments(c)

    cx = int(M['m10'] / M['m00'])

    cy = int(M['m01'] / M['m00'])
    '''
    # If myself is the biggest object on screen, find next one
    if (cx + 20 == (width / 2) or cx - 20 == (width / 2) and
            cy + 20 == (height / 2) or cy - 20 == (height / 2)):
        print('Found self, finding another')
        contours.remove(c)
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])'''

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
    
def move_away_from(x, y):
    new_x = width - x
    new_y = height - y
    pyautogui.moveTo(new_x, new_y, 0)


def detect_edges():
    with mss() as sct:
        monitor = {"top": 40, "left": 0, "width": width, "height": height}
        # sct.shot()

        # last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = np.array(sct.grab(monitor))

        # Display the picture
        # cv2.imshow("OpenCV/Numpy normal", img)

        # Display the picture in grayscale
        # cv2.imshow('OpenCV/Numpy grayscale',
        #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

        # print("fps: {}".format(1 / (time.time() - last_time)))

        # img = cv2.imread('monitor-1.png')
        edges = cv2.Canny(img, 100, 200)

        # Find the contours of the frame

        contours, hierarchy = cv2.findContours(edges.copy(), 1, cv2.CHAIN_APPROX_NONE)
        return contours


def alpha_protocol():
    cx, cy = pyautogui.position()
    keepGoing = 0
    while keepGoing < 3:
        # Detect edges
        contours = detect_edges()

        # Find coordinates for biggest shape on screen
        cx, cy, c = find_biggest_thing(contours)

        # On game over screen
        if (cx == 959 and cy == 382)\
                or (cx == 959 and cy == 352)\
                or (cx == 959 and cy == 312):
            # print('upped')
            keepGoing += 1
        else:
            # print('downed')
            keepGoing = 0
        # print(keepGoing)

        # If biggest thing is bigger than a threshold, turn around
        if cv2.contourArea(c) > 3000:
            if(cx >= 1851 and cy >= 971):
                print("Map found")
            else:
                print("Snake size ", cv2.contourArea(c), " at ", cx, cy)
                # Move away from biggest shape
                move_away_from(cx, cy)
        # Else, just go there
        else:
            pyautogui.moveTo(cx, cy)
            print("Snack size ", cv2.contourArea(c), " at ", cx, cy)


def beta_protocol():
    time.sleep(5)
    with mss() as sct:
        monitor = {"top": 40, "left": 0, "width": width, "height": height}
        # Get raw pixels from the screen, save it to a Numpy array
        # 1. Take screenshot and canny detect shapes
        # contours = detect_edges()

        img = np.array(sct.grab(monitor))
        v = np.median(img)

        # ---- apply automatic Canny edge detection using the computed median----
        lower = int(max(0, (1.0 - .33) * v))
        upper = int(min(255, (1.0 + .33) * v))
        edges = cv2.Canny(img, 100, 200)
        cv2.MORPH_CROSS

        # Find the contours of the frame

        contours, hierarchy = cv2.findContours(edges.copy(), 1, cv2.CHAIN_APPROX_NONE)

        '''
        2. Detect 5 largest shapes, 3 methods to do so
            a. Search
                i.  Init largest[5] to hold coordinates for 5 largest objects.
                ii. Search contours list and compare with largest[5]
                iii.If anything we come across is larger than something in the list, swap for smallest in list.
            b.  Sort and return
                i.  Run quicksort on list of contours
                ii. Return contours[0..4]
            c.  Pop
                i.  While largest[].length <= 5
                ii. Find largest shape in list of contours
                iii.Add to largest[]
                iv. Remove from list of contours
        '''
        # 2. Sort list of contours by size, return 5 largest
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
        # 3.  Enclose 5 largest shapes in circles
        for contour in contours:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(edges, center, radius, (0, 255, 0), 2)

        '''
        4. Find bad angles
        Given centerpoint of object = x2, y2
        Given centerpoint of screen = x1, y1
        a. H = sqrt ( (x2 - x1)^2 + (y2 - y1)^2 )
        C = arctan( delta y / delta x ) + (( x2 < widthOfScreen/2 ) ? +180 : nothing) 
        b. given radius and angle to the circle C, bad angle = C +-( 90 - (arccos( r/h ))
        slap groups into consolidator, resolve overlapping circles
        find biggest remaining safe angle
        '''


        plt.subplot(121), plt.imshow(img, cmap='gray')
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(edges, cmap='gray')
        plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

        plt.show()
        '''
        4.  Draw tangent lines from center of screen to both sides of each circle
            a.
                i.  For each circle
                ii. Draw 2 tangent lines clockwise starting at right side of top circle
                iii.Return lines[]
        5.  Find area of escape routes
            a.
                i.  int x = 0; While x < lines[].length
                ii. Distance = lines[x].endpoint - lines[x+1].endpoint
        6.  Move mouse to midpoint of linepair with largest area
        '''

def gamma_protocol():
    time.sleep(5)
    with mss() as sct:
        monitor = {"top": 40, "left": 0, "width": math.floor((width/2)), "height": height}
        # Get raw pixels from the screen, save it to a Numpy array
        # 1. Take screenshot and canny detect shapes
        # contours = detect_edges()

        img = np.array(sct.grab(monitor))
        v = np.median(img)

        # ---- apply automatic Canny edge detection using the computed median----
        lower = int(max(0, (1.0 - .33) * v))
        upper = int(min(255, (1.0 + .33) * v))
        edges = cv2.Canny(img, 100, 200)
        cv2.MORPH_CROSS

        # Find the contours of the frame

        contours, hierarchy = cv2.findContours(edges.copy(), 1, cv2.CHAIN_APPROX_NONE)

        '''
        2. Detect 5 largest shapes, 3 methods to do so
            a. Search
                i.  Init largest[5] to hold coordinates for 5 largest objects.
                ii. Search contours list and compare with largest[5]
                iii.If anything we come across is larger than something in the list, swap for smallest in list.
            b.  Sort and return
                i.  Run quicksort on list of contours
                ii. Return contours[0..4]
            c.  Pop
                i.  While largest[].length <= 5
                ii. Find largest shape in list of contours
                iii.Add to largest[]
                iv. Remove from list of contours
        '''
        # 2. Sort list of contours by size, return 3 largest
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:3]
        # 3.  Enclose 5 largest shapes in circles
        for contour in contours:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(edges, center, radius, (0, 255, 0), 200)

        '''
        4. Draw 8 compass lines from center of screen, these will be our 'feelers'
        5. numpy.bitwise_and for a binary and operation for each line with each circle
        6. This will give 8 arrays containing intersection points for each line.
        7. Remove duplicate points on lines, keeping the point closest to center
        8. Draw a polygon given points on lines.
        9. Find the polygon line with biggest length.
        10. Move towards center of that polygon line
        11. Rinse and repeat
        '''

        plt.subplot(121), plt.imshow(img, cmap='gray')
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(edges, cmap='gray')
        plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

        plt.show()

main()
