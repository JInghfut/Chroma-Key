from __future__ import print_function
import cv2 as cv
import os
import numpy as np
import argparse
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser()
parser.add_argument('--input', 
                    type=str,
                    help='input video name.', 
                    default=0
                    )
parser.add_argument('--algo',  
                    type=str, 
                    help='specify operation to be performed ie merge or split', 
                    default='split')
parser.add_argument('--dir', 
                    type=str, 
                    help='Path to directory', 
                    default='result')
parser.add_argument('--fps', 
                    type=float, 
                    help='fps for video', 
                    default=10)
args = parser.parse_args()
def split(capture, fps, dest):
    i=0
    os.mkdir(dest)
    while capture.isOpened():
        ret, frame = capture.read()
        if frame is None:
            break
        i=i+1
        cv.imshow('Frame', frame)
        cv.imwrite(dest+ "/" + str(i)+".jpg", frame)

        keyboard = cv.waitKey(1)
        if keyboard == 'q' or keyboard == 27:
            break

def merge(source, v_n, fps):
    image_folder = source
    video_name = v_n

    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    frame = cv.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    images = sorted(images)
    video = cv.VideoWriter(video_name, 0,fps, (width,height))
    for i in range(1,len(images)):
        #print(os.path.join(image_folder, image))
        frame = cv.imread(os.path.join(image_folder, str(i)+".jpg"))
        video.write(frame)
        cv.imshow('f',frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cv.destroyAllWindows()
    video.release()
    
if args.algo=='split':
    if args.input==0:
        capture = cv.VideoCapture(0)
    else:
        capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))
    if not capture.isOpened:
        print('Unable to open: ' + args.input)
        exit(0)
    split(capture, args.fps, args.dir)
else:
    merge(args.dir, args.input, args.fps)
