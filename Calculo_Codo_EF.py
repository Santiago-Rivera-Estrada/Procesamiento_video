import cv2 as cv
import numpy as np
import time
import DeteccionCodoEF as DC
cap=cv.VideoCapture("C:/Users/santi/Downloads/video1.mp4")
img=cv.imread("C:/Users/santi/Downloads/video1.mp4")
detector=DC.Detector_Pose()
while True:
    img=detector.Encontrar_Pose(img)
    cv.imshow("video", img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
