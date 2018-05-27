import os
import numpy as np
import cv2

# intencity histogram
def i_histo(img, mask=None):
    histo = []

    if mask is not None:
        img = img[mask > 0]

    for i in range(256):
        histo.append(np.sum(img[img == i]))

    return histo

# horizontal histogram
def h_histo(img):
    histo = []
    for q in range(int(img.shape[1]/1)):
        histo.append(np.sum(img[:,q:q+1] > 0))
    return np.array(histo)

# threshold an image based on rgb colors intencity
def threshold(img, lower, upper):
    mask = cv2.inRange(img, lower, upper)
    return mask


