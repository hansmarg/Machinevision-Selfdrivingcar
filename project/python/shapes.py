import os
import numpy as np
import cv2

def trapazoid(a, b, center, height, y):
    return np.matrix([[int(center - a), int(         y)],  # point1
                      [int(center + a), int(         y)],  # point2
                      [int(center + b), int(y + height)],  # point3
                      [int(center - b), int(y + height)]]) # point4

def rectangle(height, width):
    return np.matrix([[ int(     0) , int(    0) ],  # point1
                      [ int(height) , int(    0) ],  # point2
                      [ int(height) , int(width) ],  # point3
                      [ int(     0) , int(width) ]]) # point4

def draw_polygon(img, fig, color=(255,255,255), thickness=1, t=8, shift=0, close=True):
    points = np.matrix(fig)

    if len(points) <= 1:
        return

    if close==True:
        points = np.vstack([points, points[0]])

    a = points[0]
    for b in points[1:]:
        cv2.line(img, (int(a[0,0]), int(a[0,1])), (int(b[0,0]), int(b[0,1])), color, thickness)
        a = b

def fill_polygon(img, fig, color=(255,255,255)):
    points = np.matrix(fig)
    cv2.fillPoly(img, pts=[points], color=color)

def plot(canvas, plot, y_max=None, color=(255,0,0), thickness=2):

    h = canvas.shape[0]
    w = canvas.shape[1]

    if y_max is None:
        y_max = np.max(plot)

    plot = plot/y_max * h

    l = len(plot)
    bw = w/l

    for x in range(l-1):
        v = plot[x]

        p1 = ( int(    x*bw) , int(  h - plot[x]) )
        p2 = ( int((x+1)*bw) , int(h - plot[x+1]) )

        cv2.line(canvas, p1, p2, color, thickness)
