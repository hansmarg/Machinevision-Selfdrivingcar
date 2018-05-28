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

# find centers of horizontal histograms
def h_histo_peaks(histo, clearence):
    pts = []
    for i in range(len(histo)-1):
        if histo[i] - histo[i+1] > 0:
            pts.append(i)

    for i in range(len(pts)-1):
        if pts[i+1] < pts[i]+clearence:
            pts[i] = 0

    pts = np.array(pts)
    return pts[np.where(pts > 0)]

# threshold an image based on rgb colors intencity
def threshold(img, lower, upper, mask=None):

    ret = img
    if mask is not None:
        ret = np.copy(img)
        ret[mask == 0] = 0

    ret = cv2.inRange(ret, lower, upper)
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

#def dynamic_threshold(h, a, max_i=None):
#
#    if max_i is None:
#        max_i = len(h)-2
#
#    for i in range(max_i, 0, -1):
#        d = h[i] - h[i+1]
#        if d > 0:
#            return i

# event_handler for making threshold graphs clickable
_plot_threshold = 0
def threshold_plot_event_handler(event, x, y, flags, param):
    global _plot_threshold
    if event == cv2.EVENT_LBUTTONDOWN:
        _plot_threshold = x

def plot_threshold(w=1):
    return _plot_threshold/w

def find_lane_points(img, grid):
    img_h  = img.shape[0]
    cell_h = img_h/grid[0]

    for i in range(1, grid[0]):
        img[ int(cell_h*i - 1) : int(cell_h*i + 1), :] += 255

    clearence = int(img.shape[1]/grid[1])
    pic_lane_points = []
    split = np.vsplit(img, 6)

    points_grid = np.zeros((grid[0], grid[1], 2), dtype=np.int16)

    for i in range(len(split)):
        cell = split[i]

        cell_histo = h_histo(cell, 1)

        cell_histo[cell_histo > 4] = 10
        cell_histo[cell_histo <= 4] = 0

        cell_lane_points = h_histo_peaks(cell_histo, clearence)

        pic_lane_points.append(cell_lane_points)

    cell_h = int(cell_h)
    cell_h2 = int(cell_h/2)
    for i in range(len(pic_lane_points)):
        pts = pic_lane_points[i]
        if pts is not None:
            for pt in pts:
                p_x = pt
                p_y = i*cell_h + cell_h2
                p_cords = np.array([p_x, p_y], dtype=np.uint16)

                points_grid[int(p_y/cell_h),int(p_x/clearence)] = p_cords

    line_l = np.max(points_grid[:,1:3,:], axis=1)
    line_r = np.max(points_grid[:,3:5,:], axis=1)

    return line_l, line_r
