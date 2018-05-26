import sys
import cv2
import numpy as np

# turns csv file to frames with data labels
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


        tmp_arr = [1]
        tmp_arr += (np.array(data[1:5], dtype=np.int32)*scale).tolist()

        if data[6] == '\"car\"':
            tmp_arr += [1, 0, 0]
        elif data[6] == '\"trafficLight\"':
            tmp_arr += [0, 1, 0]
        elif data[6] == '\"truck\"':
            tmp_arr += [0, 0, 1]

        if len(tmp_arr) > 5:
            data_vector.append(tmp_arr)

        #cv2.rectangle(img, (int(data[1]), int(data[2])), (int(data[3]), int(data[4])), (0,255,0),10)


# turns frames and frame-labels to useful training data
def frames2data(img, data, grid_size, anchors):

    img_shape = img.shape
    bh = int(img_shape[0]/grid_size[0])
    bw = int(img_shape[1]/grid_size[1])

    data = np.matrix(data)

    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            y0, y1 = bh*i, bh*(i+1)
            x0, x1 = bw*j, bw*(j+1)

            box = img[y0:y1, x0:x1]
            print(data)

            yield box, j


# turns csv file directly into traning data
def csv2data(filepath, grid_size, anchors, start_frame=None, scale=1):

    for img, data in csv2frames(filepath, start_frame, scale):
        for x, y in frames2data(img, data, grid_size, anchors):
            yield x, y

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("ERROR: no input file")
        exit(1)

    cv2.namedWindow("data_video_show")

    path = sys.argv[1]

    key = -1
    pause = False
    for img, data in csv2frames(path, None, 0.5):


        for objects in data:
            color = (np.array(objects[5:8])*255).tolist()
            cv2.rectangle(img, (int(objects[1]), int(objects[2])), (int(objects[3]), int(objects[4])), color, 2)
            #img[int(objects[2]):int(objects[4]), int(objects[1]):int(objects[3])] = color

        for x, y in frames2data(img, data, (1, 1), 5):

            cv2.imshow('data_video_show', x)

            key = cv2.waitKey(25)
            if key == 32:
                pause = True
            elif key > -1:
                break

        if pause == True:
            key = cv2.waitKey(0)
            if key == 32:
                pause = False
            elif key > -1:
                break
        elif key > -1:
            break
#
#    for img, data in csv2frames(path, None, 0.5):
#
#        for fack in data:
#            color = (np.array(fack[5:8])*255).tolist()
#            cv2.rectangle(img, (int(fack[1]), int(fack[2])), (int(fack[3]), int(fack[4])), color, 1)
#
#        cv2.imshow('data_video_show', img)
#
#        #im_dst = cv2.warpPerspective(img.copy(), h, (600,600))
#        #cv2.imshow('perspective', im_dst)
#
#        key = cv2.waitKey(25)
#        if key > -1:
#            break

    # destroy all windows
    cv2.destroyWindow("data_video_show")



