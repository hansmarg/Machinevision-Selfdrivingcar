#include <opencv2/opencv.hpp>
#include <iostream>
#include <time.h>

#include "includes/shapes.hpp"

//using namespace cv;
//using namespace std;

static int diffclock_ms(clock_t clock1, clock_t clock2){
    double diffticks=clock1-clock2;
    double diffms=(diffticks)/(CLOCKS_PER_SEC/1000);
    return (int)diffms;
}

int main(int argc, char* argv[])
{
    std::string video_path = "../../dataset/project_video.mp4";

    // flag default values
    bool flag_autoplay = false;
    bool flag_speedup = false;
    bool flag_stable_trap = false;

    // parse arguments
    for(int i=1; i<argc; i++){
        if(strcmp(argv[i], "--autoplay") == 0){
            flag_autoplay = true;
        }
        else if(strcmp(argv[i], "--speedup") == 0){
            flag_speedup = true;
        }
        else if(strcmp(argv[i], "--stable_trap") == 0){
            flag_stable_trap = true;
        }
        else{
            video_path = argv[i];
        }
    }

    // open the video file for reading
    cv::VideoCapture cap(video_path);

    // if not success, exit program
    if (cap.isOpened() == false)
    {
        std::cout << "Cannot open the video file: " << video_path << std::endl;
        std::cin.get(); //wait for any key press
        return -1;
    }

    // Uncomment the following line if you want to start the video in the middle
    //cap.set(CAP_PROP_POS_MSEC, 300);

    // get the frames rate of the video
    double fps = cap.get(cv::CAP_PROP_FPS);
    std::cout << "Frames per seconds : " << fps << std::endl;

    // set the wait time between each frame
    int wait_time = 1000/fps;
    if(flag_speedup) wait_time = 6;

    // get height and width
    int frame_h = cap.get(cv::CAP_PROP_FRAME_HEIGHT);
    int frame_w = cap.get(cv::CAP_PROP_FRAME_WIDTH);

    // create windows
    std::string video_window_name = "DASH CAM";
    cv::namedWindow(video_window_name/*, cv::WINDOW_NORMAL*/); //create a window

    // create source points for polygon and transform
    int a;
    int b;
    int t_center;
    int t_height;
    int t_y;

    if(flag_stable_trap){
        a = 140;
        b = 800;
        t_center = cvRound(frame_w/2);
        t_height = 205;
        t_y = frame_h - t_height - 60;
    }else{
        a = 140 - 50;
        b = 460 + 80;
        t_center = cvRound(frame_w/2);
        t_height = 220;
        t_y = frame_h - t_height - 60;
    }

    std::vector<cv::Point> pts_src = shapes::trapazoid( a, b, t_center, t_height, t_y);

    // destination points for transform
    cv::Size warp_img_size(400, 400);
    std::vector<cv::Point> pts_dst = shapes::rectangle( warp_img_size.width , warp_img_size.height );

    // Calculate Homography
    cv::Mat h = findHomography(pts_src, pts_dst);

    // Output image
    cv::Mat im_out;

    // polygon figure
    cv::Mat mask(frame_h, frame_w, CV_8UC3, cv::Scalar(1,1,1));
    shapes::draw_polygon(mask, pts_src);

    // time calculation
    clock_t time_s;
    time_s = clock();

    while (true)
    {
        cv::Mat frame;
        bool bSuccess = cap.read(frame); // read a new frame from video

        //Breaking the while loop at the end of the video
        if (bSuccess == false)
        {
            std::cout << "Found the end of the video" << std::endl;
            break;
        }

        // Warp source image to destination based on homography
        cv::warpPerspective(frame, im_out, h, warp_img_size);

        // add trapazoid outline to frame
        cv::Mat marked_img = frame.mul(mask);

        // add pictures on top of big marked_img
        im_out.copyTo(marked_img(cv::Rect(marked_img.cols - im_out.cols - 20, 20 , im_out.cols, im_out.rows)));

        //show the frame in the created window
        cv::imshow(video_window_name, marked_img);

        //wait for for 10 ms until any key is pressed.
        //If the 'Esc' key is pressed, break the while loop.
        //If the any other key is pressed, continue the loop
        //If any key is not pressed withing 10 ms, continue the loop

        // time end
        int ms = diffclock_ms(clock(), time_s);
        int wait = wait_time - ms;
        printf("calculation time: %dms | wait: %dms\n", ms, wait);

        wait = (wait > 0) ? wait : 1 ;

        if (cv::waitKey(flag_autoplay ? wait : 0 ) == 27)
        {
            std::cout << "Esc key is pressed by user. Stoppig the video" << std::endl;
            break;
        }
        time_s = clock();
    }

    // destroy the created window
    //cv::destroyWindow(video_window_name);
    //cv::destroyWindow(trans_window_name);

    return 0;

}
