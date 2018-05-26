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


        # xmin, ymin, xmax, ymax
        xyxy = np.array(data[1:5], dtype=np.int32)*scale

        w = xyxy[2]-xyxy[0] # width
        h = xyxy[3]-xyxy[1] # height

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


# turns frames and frame-labels to useful training data
def frames2data(img, data, grid_size, anchors):

    img_shape = img.shape

    ch = int(img_shape[0]/grid_size[0])
    cw = int(img_shape[1]/grid_size[1])

    data = np.matrix(data)
    n_anchors = anchors.shape[0]
    object_len = (data.shape[1]+1)
    label_len  = n_anchors * object_len

    # loop for each grid cell
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):

            # calc start and
            y0, y1 = ch*i, ch*(i+1)
            x0, x1 = cw*j, cw*(j+1)

            # get cell cell from img
            cell = img[y0:y1, x0:x1]

            # extract relevant bboxes for cell
            a = np.logical_and(x0+1 <= data[:,0], data[:,0] <= x1)
            b = np.logical_and(y0+1 <= data[:,1], data[:,1] <= y1)
            i_map  = np.where(np.logical_and(a, b)) # index map over booleans
            bboxes = data[i_map[0],:]

            # normalize data relative to cell
            bboxes[:, 0] = (bboxes[:, 0] - x0) / cw
            bboxes[:, 1] = (bboxes[:, 1] - y0) / ch
            bboxes[:, 2] /= cw
            bboxes[:, 3] /= ch

            # add column of ones to bboxes
            bboxes = np.hstack([np.matrix(np.ones((bboxes.shape[0],1))), bboxes])

            # prep label tensor
            label = np.zeros(label_len)

            # fill label tensor
            for bbox in bboxes:
                iou, iou_index = 0, -1

                for k in range(n_anchors):
                    anch = anchors[k]

                    intersec = np.min(bbox[1,3], anch[0,0]) * np.min(bbox[0,4], anch[0,1])
                    tot_area = bbox[0,3]*bbox[0,4] + anch[0,0]*anch[0,1] - intersec

                    tmp_iou = intersec/tot_area
                    if tmp_iou > iou:
                        iou = tmp_iou
                        iou_index = k

                if iou_index > -1:
                    label[k*object_len : (k+1)*object_len] = bbox

            yield cell, label


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

    anchors = np.matrix([[1, 1],
                         [0.5, 0.5]])

    key = -1
    pause = False
    for img, data in csv2frames(path, None, 0.5):

        for objects in data:
            color = (np.array(objects[4:7])*255).tolist()
            w_2 = int(objects[2]/2)
            h_2 = int(objects[3]/2)
            cv2.rectangle(img, (int(objects[0]) - w_2, int(objects[1]) - w_2), (int(objects[0]) + w_2, int(objects[1]) + w_2), color, 2)
            cv2.rectangle(img, (int(objects[0]) - 1, int(objects[1]) - 1), (int(objects[0]) + 1, int(objects[1]) + 1), color, 2)
            #img[int(objects[2]):int(objects[4]), int(objects[1]):int(objects[3])] = color

        for x, y in frames2data(img, data, (2, 2), anchors):

            cv2.imshow('data_video_show', x)

            print(y.tolist())

            key = -1
            if pause == True:
                key = cv2.waitKey(0)
            else:
                key = cv2.waitKey(25)

            if key == 32:
                pause = not pause
            elif key == 13:
                pass
            elif key > -1:
                cv2.destroyWindow("data_video_show")
                exit(0)
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



