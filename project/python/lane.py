import os
import numpy as np
import cv2
import time
import math

import shapes
import lanefinder

def main():
    video_path = "../../../dataset/project_video.mp4"

    # open the video file for reading
    cap = cv2.VideoCapture(video_path)

    # if not success, exit program
    if cap.isOpened() == False:
        print("Cannot open the video file:", video_path)
        exit(-1)

    # Uncomment the following line if you want to start the video in the middle
    #cap.set(cv2.CAP_PROP_POS_MSEC, 300);

    # get the frames rate of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("Frames per seconds:", fps)

    # set the wait time between each frame
    wait_time = 1000/fps;

    # get height and width
    frame_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT);
    frame_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH);

    # create windows
    cv2.namedWindow("video_window", cv2.WINDOW_NORMAL)
    cv2.namedWindow("warp_window")

    # create source points for polygon and transform

    a = 140
    b = 800
    t_center = np.round(frame_w/2)
    t_height = 205
    t_y = frame_h - t_height - 60

    pts_src = shapes.trapazoid( a, b, t_center, t_height, t_y)

    # destination points for transform
    warp_img_size = (600, 600)
    pts_dst = shapes.rectangle( warp_img_size[0] , warp_img_size[1] )

    # Calculate Homography
    h, status = cv2.findHomography(pts_src, pts_dst)

    """
    # Output image
    im_out
    """

    # polygon figure
    mask = np.matrix(np.ones((int(frame_h), int(frame_w))), dtype=np.int8)
    shapes.draw_polygon(mask, pts_src)

    """
    # time calculation
    clock_t time_s;
    time_s = clock();
    """

    color_basis = 256
    color_basis = np.uint8(256/color_basis)

    key = -1
    pause = False
    start_time = time.time()*1000
    while True:

        # read a new frame from video
        ret, frame = cap.read()

        # breaking the while loop at the end of the video
        if ret == False:
            print("Found the end of the video")
            break

        # warp source image to destination based on homography
        im_out = cv2.warpPerspective(frame, h, warp_img_size)

        im_out = np.round(im_out/color_basis).astype(np.uint8)
        im_out = im_out*color_basis

        im_out = lanefinder.threshold(im_out, np.array([0,0,180]), np.array([255,255,255]))

        # draw trapazoid on the frame
        shapes.draw_polygon(frame, pts_src, color=(0,0,0), thickness=6)

        # show the frame in the created window
        cv2.imshow("video_window", frame);

        grid = (6,6)



        #------------------------------------------------------------------------------
        blank_img = np.zeros((im_out.shape[0],im_out.shape[1],3), np.uint8)
        blank_img[im_out > 0] = (255,255,255)

        line_l, line_r = lanefinder.find_lane_points(im_out, grid)

        for p in line_r:
            cv2.line(blank_img, (p[0]-4, p[1]), (p[0]+4, p[1]), (255,0,0), 6)
        for p in line_l:
            cv2.line(blank_img, (p[0]-4, p[1]), (p[0]+4, p[1]), (0,255,0), 6)

        cv2.imshow("gogibogi", blank_img)

        poly_l = np.polyfit(line_l[:,0]+0.1, line_l[:,1]+0.1, deg = 2, rcond=None, full=False, w=None, cov=False)
        poly_r = np.polyfit(line_r[:,0]+0.1, line_r[:,1]+0.1, deg = 2, rcond=None, full=False, w=None, cov=False)

        mat = np.zeros([600,600], dtype=np.uint8)

        l_array = []
        r_array = []

        for x in range(np.min(line_l[:,0]), np.max(line_l[:,0])):
            y = int(poly_l[0]*x**2 + poly_l[1]*x + poly_l[2])
            #y = int(poly_l[0]*x + poly_l[1])

            if 0 < y < 600 and 100 < x < 500: 
                mat[y, x] = 255
                l_array.append((x,y))
        #l_array.append((np.max(line_l[:,0]),599))

        for x in range(np.min(line_r[:,0]), np.max(line_r[:,0])):
            #y = int(poly_r[0]*x + poly_r[1])
            y = int(poly_r[0]*x**2 + poly_r[1]*x + poly_r[2])

            if 0 < y < 600 and 100 < x < 500: 
                mat[y, x] = 255
                r_array.append((x,y))
        #r_array.append((np.max(line_r[:,0]),599))

        #for x in range(np.min(line_r[:,0]), np.max(line_r[:,0])):
        #    print([int(poly_r[0]*np.power(x,2) + poly_r[1]*x + poly_r[2]), x])
        shapes.draw_polygon(mat, r_array, color=(255,255,255), thickness=1, t=8, shift=0, close=False)
        shapes.draw_polygon(mat, l_array, color=(255,255,255), thickness=1, t=8, shift=0, close=False)

        cv2.imshow("ASDASD", mat)
        #print(poly_l)
        

        #-------------------------------------------------------------------------------


        # calculate time it takes to do homo transform
        calc_time = (time.time()*1000) - start_time
        wait = wait_time

        # calculate waiting time to maintain fps
        if int(wait) > calc_time:
            wait -= calc_time
            wait = int(wait)
            if wait == 0:
                wait = 1
        else:
            wait = 1

        # wait for frame
        key = -1
        if pause == True:
            key = cv2.waitKey(0)
        else:
            key = cv2.waitKey(wait)

        if key == 32:
            pause = not pause
        elif key == 13:
            pass
        elif key > -1:
            # destroy the created window
            cv2.destroyAllWindows()
            exit(0)

        # get start time for calculating wait_time next iteration
        start_time = time.time()*1000


# run main function
if __name__ == '__main__':
    main()
