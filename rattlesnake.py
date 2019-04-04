import pyautogui

width, height = pyautogui.size()

def main():
	#while(true):
		#do the thing

def moveToCenter():
	pyautogui.moveTo(width / 2, height / 2)	
	
def turnAround():
	currentPosition = pyautogui.position()
	if(currentPosition.y < height / 2)
		#increase height
		heightDiff 	= height - currentPosition.y
	else
		#decrease height
	
	if(currentPosition.x < width / 2)
		#increase width
	else
		#decrease width