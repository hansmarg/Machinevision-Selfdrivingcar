#include <opencv2/opencv.hpp>
#include <iostream>
//#include "debug_stuff.cpp"

using namespace cv;
using namespace std;

//int main(int argc, char** argv)
int main(int argc, char* argv[])
{
    std::string img_path;

    // check for failure
    if(argc < 2){
        img_path = "../crap/test1.jpg";
    }else{
        img_path = argv[1];
    }

    // Read the image file
    cv::Mat image = cv::imread(img_path);

    // check for failure
    if(image.empty()){
        std::cout << "Could not open or find image: " << img_path << std::endl;
        return 1;
    }

    //debug_stuff::print_cvmat_type(image);

    // create windowName before window (for learning purposes)
    std::string windowName = "fack this life";

    // create the window
    cv::namedWindow(windowName);

    // show the image inside the window
    cv::imshow(windowName, image);

    // wait for any keystroke
    cv::waitKey(0);

    // do hit to image
    //cv::GaussianBlur(image, image, cv::Size(3,3), 10, 10);
    //image /= 64;
    //image *= 64;

    cv::Scalar min_color = cv::Scalar(0,200,200);
    cv::Scalar max_color = cv::Scalar(255,255,255);
    cv::inRange(image, min_color,  max_color, image);

    // show the image inside the window
    cv::imshow(windowName, image);

    // wait for any keystroke
    cv::waitKey(0);

    // destroy the created window
    cv::destroyWindow(windowName);

    return 0;
}
