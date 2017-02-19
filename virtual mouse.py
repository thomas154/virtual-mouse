import imutils
import cv2
import pyautogui
import numpy as np
from collections import deque
from pymouse import PyMouse
m=PyMouse()
ptsx=deque()
ptsy=deque()
x=0
y=0
greenLower = (38, 80, 50)
greenUpper = (75, 255, 255)
#greenLower =(0,91,75)
#greenUpper =(58,255,255)
#yellowLower=(0,91,75)
#yellowUpper=(58,255,255)
camera = cv2.VideoCapture(0)
while True:
	(grabbed, frame) = camera.read()
	frame=cv2.flip(frame,1)
	frame = imutils.resize(frame, width=1366)
	blurred = cv2.GaussianBlur(frame, (27, 27), 200)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	#cnts1 = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	if len(cnts)>0:
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if radius > 10:
			#cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			a,b=center
			ptsx.appendleft(a)
			ptsy.appendleft(b)
			if len(ptsx)>2 and len(ptsy)>2:
				ptsx.pop()
				ptsy.pop()
			x=int(np.average(ptsx))
			y=int(np.average(ptsy))
			#pyautogui.moveTo(2*(x-(1366/2)),3*(y-(768/2)));
			m.move(x,y)
			m.move(x,y)
			m.move(x,y)
			m.move(x,y)
			#print len(cnts)
	cv2.imshow("Blesson", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
	#print c
	
camera.release()
cv2.destroyAllWindows()
