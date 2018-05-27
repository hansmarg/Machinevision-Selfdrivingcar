import os
import numpy as np
import cv2

def red_histo():
    pass

def i_histo(img):
    i_histo = []
    for q in range(int(img.shape[1]/1)):
        i_histo.append(np.sum(img[:,q:q+1] > 0))
    return np.array(i_histo)

def threshold(img, lower, upper):
    mask = cv2.inRange(img, lower, upper)
    return mask


