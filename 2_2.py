from __future__ import print_function
import cv2 as cv
import os
import numpy as np
import argparse
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, help='Path to directory', default='result')
args = parser.parse_args()

capture = cv.VideoCapture(0)
i=0
os.mkdir(args.dir)
while True:
    ret, frame = capture.read()
    if frame is None:
        break
    i=i+1
    cv.imshow('Frame', frame)
    cv.imwrite(args.dir +"/"+ str(i)+".jpg", frame)

    keyboard = cv.waitKey(1)
    if keyboard == 'q' or keyboard == 27:
        break
