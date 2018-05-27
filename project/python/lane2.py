import os
import numpy as np
import cv2
import time

import shapes
import lanefinder

SCALE=0.5

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
    frame_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)*SCALE;
    frame_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)*SCALE;

    # create windows
    cv2.namedWindow("video_window")
    cv2.namedWindow("plot_window")
    cv2.setMouseCallback("plot_window", lanefinder.threshold_plot_event_handler)

    # create source points for polygon and transform

    a = 140*SCALE
    b = 800*SCALE
    t_center = np.round(frame_w/2)
    t_height = 205*SCALE
    t_y = (frame_h - t_height - 60*SCALE)

    pts_src = shapes.trapazoid( a, b, t_center, t_height, t_y)

    # destination points for transform
    warp_img_size = (600, 600)
    pts_dst = shapes.rectangle( warp_img_size[0] , warp_img_size[1] )

    # polygon figure
    mask = np.matrix(np.zeros((int(frame_h), int(frame_w))), dtype=np.uint8)
    shapes.fill_polygon(mask, pts_src, (1, 1, 1))

    # calculate factor for making simpler color pallatte
    color_basis = 256 # change this in case you want less than 256 colors
    color_basis = np.uint8(256/color_basis)

    # variables for loop run
    key = -1
    pause = False
    start_time = time.time()*1000

    # loop through video
    while True:

        # read a new frame from video
        ret, frame = cap.read()

        # breaking the while loop at the end of the video
        if ret == False:
            print("Found the end of the video")
            break

        # get frame
        frame = cv2.resize(frame, None, fx=SCALE, fy=SCALE, interpolation = cv2.INTER_CUBIC) # resize

        # copy frame to mod it
        mframe = np.copy(frame)

        # simplify color basis
        mframe = np.round(mframe/color_basis).astype(np.uint8)
        mframe = mframe*color_basis
        mframe = cv2.bitwise_and(frame, frame, mask=mask)

        # find the intencity histogram of the red layer
        red_histo = lanefinder.i_histo(mframe[:,:,2], limit=255, mask=mask)
        red_histo = np.array(red_histo)/np.max(red_histo)*100

        # calculate threshold and threshold x position on plot
        dth = 10
        th, h = lanefinder.dynamic_threshold(red_histo, dth, 245)
        h += dth

        # prep for histogram plot
        plot = np.zeros((240, 600, 3), dtype=np.float)
        shapes.plot(plot, red_histo, y_max=300, color=(0, 0, 255), thickness=2)
        shapes.plot(plot, h, y_max=dth*2+2, color=(255, 0, 255), thickness=2)

        static_th_x = int(lanefinder.plot_threshold())
        static_th   = int(static_th_x/plot.shape[1] * 256)

        # add plot histogram
        th_x = int(th/256 * plot.shape[1])
        cv2.line(plot, (th_x,0), (th_x,plot.shape[1]), (255,0,0), 4)
        cv2.line(plot, (static_th_x,0), (static_th_x,plot.shape[1]), (0,255,0), 4)
        cv2.imshow("plot_window", plot)
        try:
            mframe1 = lanefinder.threshold(mframe, np.array([0,0,th]), np.array([255,255,255]), mask=mask)
            #mframe2 = lanefinder.threshold(mframe, np.array([0,0,static_th]), np.array([255,255,255]),mask=mask)
        except:
            print("Frame crash, internal opencv problem..")
            continue

        # show the frame in the created window
        cv2.imshow("video_window", mframe1);
        cv2.imshow("shit", mframe2);

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
        elif key == 27:
            # destroy the created window
            cv2.destroyAllWindows()
            exit(0)

        # get start time for calculating wait_time next iteration
        start_time = time.time()*1000


# run main function
if __name__ == '__main__':
    main()
