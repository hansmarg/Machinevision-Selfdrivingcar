import sys
import cv2
import numpy as np

def data_video_show(path):
    filename = path+"labels.csv"
    print("PATH:", path)
    print("FILE:", filename)


    # open file
    try:
        f = open(filename, "r")
    except FileNotFoundError as e:
        print("ERROR: file not found")
        exit(2)

    # loop through file
    current_frame = None
    img = None
    for line in f:
        data = line.split()
        frame = data[0]

        if current_frame != frame:
            img = cv2.imread(path+frame)



            current_frame = frame
            yield img, data
            #print(current_frame)

        #cv2.rectangle(img, (int(data[1]), int(data[2])), (int(data[3]), int(data[4])), (0,255,0),10)





if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("ERROR: no input file")
        exit(1)

    cv2.namedWindow("data_video_show", cv2.WINDOW_NORMAL)

    pts_src = np.array()[(652, 685), (1195, 685), (1886, 1014)]
    pts_dst = np.array([(0, 0), (600, 0), (600, 600), (0, 600)])
    h, status = cv2.findHomography(pts_src, pts_dst)

    path = sys.argv[1]
    for img, data in data_video_show(path):
        print(data[0])
        cv2.imshow('data_video_show', img)
        im_dst = cv2.warpPerspective(img.copy(), h, (600,600))
        cv2.imshow('perspective', im_dst)

        key = cv2.waitKey(25)
        if key > -1:
            break

    # destroy all windows
    cv2.destroyWindow("data_video_show")