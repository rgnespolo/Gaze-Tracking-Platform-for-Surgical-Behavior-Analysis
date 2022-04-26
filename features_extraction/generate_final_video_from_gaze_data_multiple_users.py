import cv2
import numpy as np
import csv
import pandas as pd
from scipy.spatial import distance
import glob, os    

# font
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
fontColor = (0, 255, 0)
thickness = 2
#Before continue, make sure that the gaze acquisition method and the surgical video have the same frequency (60Hz in our case)
#Read raw surgical procedure video
file_name = "raw_surgical_recordings.mp4"
cap = cv2.VideoCapture(file_name)

#Create file that will contain surgical video + gaze patterns
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('final_video_with_surgeons_gaze.avi', fourcc, 60.0, (1920,1080))


gaze_readings = pd.read_csv(r'all_experts_one_sheet.csv')
no_surgeons = gaze_readings[user].max()

for i in (range(len(gaze_readings.index))/range(len(surgeons))): #acquire total number of frames recorded
        _, frame = cap.read()
    for j in range(len(surgeons)):
        #Extract coordinates from each surgeons' gaze. 'i' is the current frame
        coord = (int(gaze_readings.iloc[i][3]), int(gaze_readings.iloc[i][4]))
        cv2.putText(frame, str('* Surgeon_' + j), coord, font,
                    fontScale, fontColor, thickness, cv2.LINE_AA)
    
    out.write(frame) #write frame with gaze coordinates

out.release()
cv2.destroyAllWindows()
f.close()
cv2.destroyAllWindows()