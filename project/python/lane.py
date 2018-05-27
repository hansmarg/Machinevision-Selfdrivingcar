import os
import numpy as np
import cv2
import time

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

        im_out_h  = im_out.shape[0]
        cell_nums = 6
        cell_h    = im_out_h/cell_nums

        for i in range(1, cell_nums):
            im_out[ int(cell_h*i - 1) : int(cell_h*i + 1), :] += 255
        cv2.imshow("warp_window", im_out)

        #cell_histo = None
        #for cell in np.vsplit(im_out, 6):

        cell = np.vsplit(im_out, 6)[-1]
        cell_histo = lanefinder.h_histo(cell)

        cell_histo[cell_histo > 4] = 10
        cell_histo[cell_histo <= 4] = 0
        cell_histo = cell_histo[::2]+cell_histo[1::2]
        cell_histo = cell_histo[::2]+cell_histo[1::2]
        print(cell_histo)

        plot = np.zeros((150, 300, 3), dtype=np.float)+255
        shapes.plot(plot, cell_histo, color=(0, 0, 0), thickness=2)
        cv2.imshow("plot_window", plot)


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
