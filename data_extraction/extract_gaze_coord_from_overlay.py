import cv2
import numpy as np
import csv
from scipy.spatial import distance


previous_coord = (0,0)
coord = (0,0)
x_previous = 0
y_previous = 0
x = 0
y = 0
#Read recorded video with gaze data (bubble overlay from the device manufacturer)
file_name = r"surgeon_1_gaze.mp4"
cap = cv2.VideoCapture(file_name)
surgeon = 11
#Create .csv that will contain the extracted gaze coordinates
f = open('file_name' + '.csv', 'a+', newline='')
writer = csv.writer(f)


while(1):
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Range of the green overlay bubble in the HSV color space
    lower_green = np.array([50, 240, 240])
    upper_green = np.array([60, 255, 255])

    # Threshold the HSV image 
    mask = cv2.inRange(hsv, lower_green, upper_green)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    # Finding contours of the bubble area
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        #Detect main bubble overlay to avoid noisy data
        if cv2.contourArea(c) > 40:
            x, y, w, h = cv2.boundingRect(c)
            #Draw rectangle over the gaze position detected for validation purposes
            cv2.rectangle(frame, (x, y), (x + w, y + h), (36, 255, 12), 2)
            coord = (int((x+(x+w))/2), int((y+(y+h))/2))
            x = (int((x + (x + w)) / 2))
            y = (int((y + (y + h)) / 2))
            dst = distance.euclidean(coord, previous_coord)
            print('Euclidean', dst)
            frame = cv2.circle(frame, coord, 3, (255,0,0), 2)
            print(coord)
        else:
            x = x_previous
            y = y_previous
        previous_coord = coord
        x_previous = x
        y_previous = y
    # Visualize the original frame, detection of gaze position, and plotted gaze coordinates detected for validation purposes
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    writer.writerow([surgeon,x,y,x_previous, y_previous, dst])

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    if k == ord('p'):
        cv2.waitKey(-1)

f.close()
cv2.destroyAllWindows()