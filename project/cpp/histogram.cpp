#include <opencv2/opencv.hpp>
#include <iostream>
#include <time.h>

#include "includes/shapes.hpp"
#include "includes/histogram.hpp"

static int diffclock_ms(clock_t clock1, clock_t clock2){
    double diffticks=clock1-clock2;
    double diffms=(diffticks)/(CLOCKS_PER_SEC/1000);
    return (int)diffms;
}

using namespace cv;
using namespace std;

int calc_threshold(cv::Mat histo, int shift=0){

    for(int i=histo.rows-2; i>=0; i++){

        float d = histo.at<float>(i) - histo.at<float>(i+1);

        if(d > 0){
            return ((i+shift)*16)-4;
        }

    }

    return 0;
}

cv::Mat forat_mask(cv::Mat img, int th_blue, int th_green, int th_red){
	cv::Mat frame = img.clone();
	cv::Mat ret;
	cv::Scalar min_color = cv::Scalar(th_blue,th_green,th_red);
	cv::Scalar max_color = cv::Scalar(255,255,255);
	cv::inRange(frame, min_color,  max_color, ret);

	return ret;
}


int mouseX = -1;
int mouseY = -1;

void CallBackFunc(int event, int x, int y, int flags, void* userdata){
    if ( flags == cv::EVENT_FLAG_LBUTTON ){
        //std::cout << "Left mouse button is clicked - position (" << x << ", " << y << ")" << std::endl;
        mouseX = x;
        mouseY = y;
    }
}

int main(int argc, char* argv[])
{
    std::string video_path = "../../dataset/project_video.mp4";

    // flag default values
    bool flag_autoplay = false;
    bool flag_speedup = false;
    bool flag_bigger_trap = false;

    // parse arguments
    for(int i=1; i<argc; i++){
        if(strcmp(argv[i], "--autoplay") == 0){
            flag_autoplay = true;
        }
        else if(strcmp(argv[i], "--speedup") == 0){
            flag_speedup = true;
        }
        else if(strcmp(argv[i], "--bigger_trap") == 0){
            flag_bigger_trap = true;
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
    //cv::namedWindow("green", cv::WINDOW_NORMAL); //create a window
    //cv::namedWindow("blue", cv::WINDOW_NORMAL); //create a window

    //set the callback function for any mouse event
    cv::setMouseCallback(video_window_name, CallBackFunc, NULL);

    // crate mask
    cv::Mat mask = cv::Mat::zeros(frame_h, frame_w, CV_8U); // all 0
    cv::Mat frame_mask = cv::Mat(frame_h, frame_w, CV_8UC3, cv::Scalar(255,0,0)); // all 0


    std::vector<cv::Point> mask_points;
    if(flag_bigger_trap){
        //mask_points = shapes::trapazoid(90, 540, cvRound(frame_w/2), 220, frame_h - 220  - 60);
        mask_points = shapes::trapazoid(350, 1800, cvRound(frame_w/2), 205, frame_h - 205 - 60);
    }else{
        //mask_points = shapes::trapazoid(90, 600, cvRound(frame_w/2), 205, frame_h - 205 - 60);
        mask_points = shapes::trapazoid( 140, 800, cvRound(frame_w/2), 205, frame_h - 265);
    }

    // craete the mask
    cv::fillConvexPoly(mask,              // Image to be drawn on
                       mask_points,            // C-Style array of points
                       1, // Color , BGR form
                       CV_AA,             // connectedness, 4 or 8
                       0);                // Bits of radius to treat as fraction

    // craete the mask
    cv::fillConvexPoly(frame_mask,              // Image to be drawn on
                       mask_points,            // C-Style array of points
                       cv::Scalar(1,1,1), // Color , BGR form
                       CV_AA,             // connectedness, 4 or 8
                       0);                // Bits of radius to treat as fraction


    int max_histo = cv::countNonZero(mask);
    printf("max_histo: %d\n", max_histo);


    // destination points for transform
    cv::Size plot_size(400, 200);
    cv::Mat b_histo, g_histo, r_histo;
    cv::Mat histo_plot;
    cv::Mat histo_plot2;
    cv::Mat histo_plot3;

    // time calculation
    clock_t time_s;
    time_s = clock();

    bool keep_frame = false;
    cv::Mat org_frame;

    int th_blue = 0, th_green = 0, th_red = 180;

    // polygon figure
    cv::Mat trap_outline(frame_h, frame_w, CV_8UC3, cv::Scalar(1,1,1));
    shapes::draw_polygon(trap_outline, mask_points);

    while (true)
    {

        if(mouseX > -1 && mouseY > -1){

            if(mouseX > (frame_w - plot_size.width - 20) && mouseX < (frame_w - 20)){
                if(mouseY > 20 && mouseY < (20 + plot_size.height)){
                    th_blue = (mouseX - (frame_w - plot_size.width - 20)) * 256 / plot_size.width;
                    std::cout << "th_blue = " << th_blue << std::endl;
                }
                else if(mouseY > (40 + plot_size.height) && mouseY < (40 + plot_size.height*2)){
                    th_green = (mouseX - (frame_w - plot_size.width - 20)) * 256 / plot_size.width;
                    std::cout << "th_green = " << th_green << std::endl;
                }
                else if(mouseY > (60 + plot_size.height*2) && mouseY < (60 + plot_size.height*3)){
                    th_red = (mouseX - (frame_w - plot_size.width - 20)) * 256 / plot_size.width;
                    std::cout << "th_red = " << th_red << std::endl;
                }
            }

            mouseX = -1;
            mouseY = -1;
            //keep_frame = true;
        }

        if(keep_frame){
            //keep_frame = false;
        }else{
            bool bSuccess = cap.read(org_frame); // read a new org_frame from video

            //Breaking the while loop at the end of the video
            if (bSuccess == false)
            {
                std::cout << "Found the end of the video" << std::endl;
                break;
            }
        }

        cv::Mat frame = org_frame.clone();

        frame /= 16;
        frame *= 16;

        // split image into planes (bgr)
        std::vector<cv::Mat> bgr_planes;
        cv::split( frame, bgr_planes );

        cv::Mat blue_frame  = bgr_planes[0];
        cv::Mat green_frame = bgr_planes[1];
        cv::Mat red_frame   = bgr_planes[2];

        // calculate histogram
        b_histo = histogram::intensity_histogram(blue_frame , mask, 16);
        g_histo = histogram::intensity_histogram(green_frame, mask, 16);
        r_histo = histogram::intensity_histogram(red_frame  , mask, 16);

        // create plot canvases
        histo_plot  = cv::Mat::zeros(plot_size.height, plot_size.width, CV_8UC3);
        histo_plot2 = cv::Mat::zeros(plot_size.height, plot_size.width, CV_8UC3);
        histo_plot3 = cv::Mat::zeros(plot_size.height, plot_size.width, CV_8UC3);

        // plot thesholds
        cv::line( histo_plot , cv::Point( (th_blue*plot_size.width / 256) , 0 ) , cv::Point( (th_blue*plot_size.width / 256) ,  plot_size.height) , cv::Scalar(255, 255, 255), 1, 8, 0  );
        cv::line( histo_plot2, cv::Point( (th_green*plot_size.width / 256) , 0 ) , cv::Point( (th_green*plot_size.width / 256) ,  plot_size.height) , cv::Scalar(255, 255, 255), 1, 8, 0  );
        cv::line( histo_plot3, cv::Point( (th_red*plot_size.width / 256) , 0 ) , cv::Point( (th_red*plot_size.width / 256) ,  plot_size.height) , cv::Scalar(255, 255, 255), 1, 8, 0  );

        //// kernel for smoothing
        //int kernel_size = 5;
        //cv::Mat kernel = cv::Mat::ones(kernel_size, 1, CV_8U); // all 0

        //// smooth blue
        //cv::Mat b_smooth;
        //filter2D(b_histo, b_smooth, -1, kernel);
        //b_smooth /= kernel_size;

        //// smooth green
        //cv::Mat g_smooth;
        //filter2D(g_histo, g_smooth, -1, kernel);
        //g_smooth /= kernel_size;

        th_red = calc_threshold(r_histo, -1);
        std::cout << "th_red = " << th_red << " | " << th_red/16 << std::endl;

        // plot original histos
        shapes::plot(histo_plot , b_histo, cv::Scalar(255,0,0), 1); //, max_histo);
        shapes::plot(histo_plot2, g_histo, cv::Scalar(0,255,0), 1); //, max_histo);
        shapes::plot(histo_plot3, g_histo, cv::Scalar(0,0,255), 1); //, max_histo);

        // plot smoothed histos
        //shapes::plot(histo_plot , b_smooth, cv::Scalar(0,0,255), 1, max_histo);
        //shapes::plot(histo_plot2, g_smooth, cv::Scalar(0,0,255), 1, max_histo);

        // add pictures on top of big frame
        frame = frame.mul(frame_mask);

        frame = forat_mask(frame, th_blue, th_green, th_red);

	    vector<Vec4i> lines;
        HoughLinesP(frame, lines, 1, CV_PI/180, 25, 30, 250 );

        //std::vector<cv::Mat> channels;
        //channels.push_back(frame);
        //channels.push_back(frame);
        //channels.push_back(frame);

        //cv::merge(channels, frame);
        //
        cv::Mat new_frame = org_frame.clone();
        new_frame = new_frame.mul(trap_outline);

        for( size_t i = 0; i < lines.size(); i++ )
        {
            Vec4i l = lines[i];
            line( new_frame, Point(l[0], l[1]), Point(l[2], l[3]), Scalar(0,0,255), 3, CV_AA);
        }

        //histo_plot.copyTo(new_frame(cv::Rect(new_frame.cols - histo_plot.cols - 20, 20 , histo_plot.cols, histo_plot.rows)));
        //histo_plot2.copyTo(new_frame(cv::Rect(new_frame.cols - histo_plot2.cols - 20, 40 + histo_plot.rows , histo_plot2.cols, histo_plot2.rows)));
        //histo_plot3.copyTo(new_frame(cv::Rect(new_frame.cols - histo_plot3.cols - 20, 60 + histo_plot.rows*2 , histo_plot3.cols, histo_plot3.rows)));

        //show the new_frame in the created window
        cv::imshow(video_window_name, new_frame);
        //cv::imshow("blue", blue_frame);
        //cv::imshow("green", green_frame);

        //wait for for 10 ms until any key is pressed.
        //If the 'Esc' key is pressed, break the while loop.
        //If the any other key is pressed, continue the loop
        //If any key is not pressed withing 10 ms, continue the loop

        // time end
        int ms = diffclock_ms(clock(), time_s);
        int wait = wait_time - ms;
        printf("calculation time: %dms | wait: %dms\n", ms, wait);

        wait = (wait > 0) ? wait : 1 ;

        int wait_key = cv::waitKey(flag_autoplay ? wait : 0 );
        if (wait_key == 27)
        {
            std::cout << "Esc key is pressed by user. Stoppig the video" << std::endl;
            break;
        }
        else if(wait_key == 112){  // p - key
            flag_autoplay = !flag_autoplay;
            keep_frame = flag_autoplay;
        }
        else if(wait_key == 32){ // space - key
            //std::cout << "h key" << std::endl;
            keep_frame = !keep_frame; //true;
        }
        //else{
        //    std::cout << "key pressed: " << wait_key << std::endl;
        //}
        time_s = clock();
    }

    // destroy the created window
    //cv::destroyWindow(video_window_name);
    //cv::destroyWindow(trans_window_name);

    return 0;

}
