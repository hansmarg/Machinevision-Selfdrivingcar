import os
import numpy as np
import cv2

# intencity histogram
def i_histo(img, limit=256, mask=None):
    histo = []

    if mask is not None:
        img = img[mask > 0]

    for i in range(limit):
        histo.append(np.sum(img[img == i]))

    return np.array(histo)

# horizontal histogram
def h_histo(img, w=1):
    histo = []
    for q in range(int(img.shape[1]/w)):
        histo.append(np.sum(img[:,q*w:(q+1)*w] > 0))
    return np.array(histo)

# threshold an image based on rgb colors intencity
def threshold(img, lower, upper, mask=None):

    ret = img
    if mask is not None:
        ret = np.copy(img)
        ret[mask == 0] = 0

    cv2.imshow("fack", ret)

    ret = cv2.inRange(ret, lower, upper)
    cv2.imshow("fack2", ret)
    return ret

# calculate the threshold to show lane lines based on the histogram
def dynamic_threshold(histo, a, max_i=None):
    h = np.copy(histo)

    h[h >= a] = a+1
    h[h < a] = 0

    if max_i is None:
        max_i = len(h)-1

    b = 100
    for i in range(max_i, 0, -1):
        if b >= h[i]:
            b = h[i]
        else:
            return i, h

    return max_i, h

# event_handler for making threshold graphs clickable
_plot_threshold = 0
def threshold_plot_event_handler(event, x, y, flags, param):
    global _plot_threshold
    if event == cv2.EVENT_LBUTTONDOWN:
        _plot_threshold = x

def plot_threshold(w=1):
    return _plot_threshold/w
