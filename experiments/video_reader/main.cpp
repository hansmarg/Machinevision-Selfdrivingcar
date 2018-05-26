#include <opencv2/opencv.hpp>
#include <iostream>

//using namespace cv;
//using namespace std;

int main(int argc, char* argv[])
{
    std::string video_path;

    // check for failure
    if(argc < 2){
        video_path = "../../dataset/project_video.mp4";
    }else{
        video_path = argv[1];
    }

    //open the video file for reading
    cv::VideoCapture cap(video_path);

    // if not success, exit program
    if (cap.isOpened() == false)
    {
        std::cout << "Cannot open the video file" << std::endl;
        std::cin.get(); //wait for any key press
        return -1;
    }

    //Uncomment the following line if you want to start the video in the middle
    //cap.set(CAP_PROP_POS_MSEC, 300);

    //get the frames rate of the video
    double fps = cap.get(cv::CAP_PROP_FPS);
    std::cout << "Frames per seconds : " << fps << std::endl;

    int wait_time = 1000/fps;

    std::string window_name = "My First Video";

    cv::namedWindow(window_name, cv::WINDOW_NORMAL); //create a window

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

        //show the frame in the created window
        cv::imshow(window_name, frame);

        //wait for for 10 ms until any key is pressed.
        //If the 'Esc' key is pressed, break the while loop.
        //If the any other key is pressed, continue the loop
        //If any key is not pressed withing 10 ms, continue the loop
        if (cv::waitKey(wait_time) == 27)
        {
            std::cout << "Esc key is pressed by user. Stoppig the video" << std::endl;
            break;
        }
    }

    // destroy the created window
    cv::destroyWindow(window_name);

    return 0;

}
