import sys
import cv2
import numpy as np



class rect():

	Xmin, Ymin, Xmax, Ymax

	def __init__(self, xmi, ymi, xma, yma):
		Xmin = xmi
		Ymin = ymi
		Xmax = xma
		Ymax = yma

	def area():
		return (Xmax - Xmin) * (Ymax - Ymin)

	def h():
		return Ymax - Ymin

	def w():
		return Xmax - Xmin


def csv2frames(filepath, start_frame=None, scale=1):

    # extract the directory of the labels.csv file
    dirpath = filepath[0: filepath.index("labels.csv")]

    # print paths to check
    print("PATH:", dirpath)
    print("FILE:", filepath)

    # try open the file
    try:
        f = open(filepath, "r")
    except FileNotFoundError as e:
        print("ERROR: file not found")
        exit(2)

    # if start_frame is set, skip to frame after
    if start_frame != None:
        for line in f:
            data = line.split() # split lines by whitespaces
            if data[0] == start_frame:
                break

    # prev vars
    current_frame = None
    data_vector = []
    img = None

    # loop through (rest of) file
    for line in f:

        data = line.split() # split lines by whitespaces
        frame = data[0]     # get frame name

        # skip obscured objects
        if data[5] == "1":
            continue

        # check if frame is new
        if frame != current_frame:

            # yield collected data
            if current_frame != None:
                yield img, data_vector

            # read new frame
            img = cv2.imread(dirpath+frame)
            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation = cv2.INTER_CUBIC) # resize

            # reset variables
            current_frame = frame
            data_vector   = []


        # xmin, ymin, xmax, ymax
        xyxy = np.array(data[1:5], dtype=np.float64)*scale

        w = xyxy[2]-xyxy[0] # width
        h = xyxy[3]-xyxy[1] # height

        print(w, h)

        x = xyxy[0] + w/2   # x_pos
        y = xyxy[1] + h/2   # y_pos

        # prep tmp_arr
        tmp_arr = [x, y, w, h]

        if data[6] == '\"car\"':
            tmp_arr += [1, 0, 0]
        elif data[6] == '\"trafficLight\"':
            tmp_arr += [0, 1, 0]
        elif data[6] == '\"truck\"':
            tmp_arr += [0, 0, 1]

        if len(tmp_arr) > 4:
            data_vector.append(tmp_arr)
