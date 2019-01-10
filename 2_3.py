from __future__ import print_function
import cv2
import os
import numpy as np
import pandas as pd
import argparse
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

low = []
high = []
parser = argparse.ArgumentParser()
parser.add_argument('--input_1', 
                    type=str, 
                    help='Path to video 1')
parser.add_argument('--input_2', 
                    type=str, 
                    help='Path to video 2')
parser.add_argument('--output', 
                    type=str, 
                    help='Path to output video', 
                    default='result.avi')
#parser.add_argument('--background', type=str, help='xyz')
args = parser.parse_args()
def restrict(color_component):
    return np.clip(color_component, 0, 255)

def calculate(frame_1):
    top_crop_y = 20
    bottom_crop_y = 359
    f_flattened = []
    f_hsv = cv2.cvtColor(frame_1, cv2.COLOR_RGB2HSV)

    for index in range(3):
        top = np.array(f_hsv[:top_crop_y, :, index]).flatten()
        bottom = np.array(f_hsv[bottom_crop_y:, :, index]).flatten()
        top_and_bottom = np.append(top, bottom)
        top_and_bottom_series = pd.Series(top_and_bottom)
        #print(top_and_bottom_series.describe())
        f_flattened.append(top_and_bottom_series)
    

    z_value = 10.0
    global low
    global high
    for i in range(3):
        mu = f_flattened[i].values.mean()
        sigma = f_flattened[i].values.std()
        deviation = z_value*sigma
        #print(mu)
        #print(deviation)
        low.append(restrict(mu-deviation-20))
        high.append(restrict(mu+deviation+20))
    print(low)
    print(high)


def chroma_key(frame_1, frame_2):
    bg_cropped = frame_2[:len(frame_1), :len(frame_1[0]), :]
    plt.imshow(frame_1)
    #print(frame_1.shape)
    #plt.show()
    
    global low
    global high
    #print(low)
    #print(high)
    mask_lower = np.array([low[0], low[1], low[2]])
    mask_higher = np.array([ high[0], high[1], high[2]])
    f_hsv = cv2.cvtColor(frame_1, cv2.COLOR_RGB2HSV)
    f_mask = cv2.inRange(f_hsv, mask_lower, mask_higher)

    masked_f = np.copy(frame_1)
    masked_f[f_mask != 0] = [0, 0, 0]

    f_hand = np.copy(frame_1)
    masked_f[f_mask != 0] = [0, 0, 0]

    bg_masked = np.copy(bg_cropped)
    bg_masked[f_mask == 0] = [0,0,0]

    full_picture = bg_masked + masked_f
    cv2.imshow('f_1',full_picture)
    return full_picture

if args.input_1 == None or args.input_2 == None:
    print("Please give input file")
    exit(0)
else:
    v1 = cv2.VideoCapture(args.input_1)
    v2 = cv2.VideoCapture(args.input_2)
    width = v1.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = v1.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = v1.get(cv2.CAP_PROP_FPS)
    ov = cv2.VideoWriter(args.output, 0,fps, (int(width),int(height)))
    i=0
    #calculate(cv2.imread(args.background))
    while v1.isOpened() and v2.isOpened():
        ret_1, frame_1 = v1.read()
        ret_2, frame_2 = v2.read()
        if i==0:
            calculate(frame_1)
            i+=1
        full_picture = chroma_key(frame_1, frame_2)
        ov.write(full_picture)
        #cv2.imshow('frame_1', frame_1)
        #cv2.imshow('frame_2', frame_2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    v1.release()
    cv2.destroyAllWindows()