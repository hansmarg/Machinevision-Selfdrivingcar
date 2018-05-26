#include <opencv2/opencv.hpp>
#include <iostream>
//#include "debug_stuff.cpp"

//using namespace cv;
//using namespace std;

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

    // (BEFORE MOD) show the image inside the window
    cv::imshow(windowName, image);

    // wait for any keystroke
    cv::waitKey(0);

    // MOD THE IMAGE
    cv::Mat mask = cv::Mat::zeros(image.rows, image.cols, CV_8UC3); // all 0

    std::vector<cv::Point> points;
    points.push_back(cv::Point(520 , 470));   //point1
    points.push_back(cv::Point(800 , 470));   //point2
    points.push_back(cv::Point(1120, 665));   //point3
    points.push_back(cv::Point(200 , 665));   //point4

    cv::fillConvexPoly(mask,              // Image to be drawn on
                       points,            // C-Style array of points
                       cv::Scalar(1,1,1), // Color , BGR form
                       CV_AA,             // connectedness, 4 or 8
                       0);                // Bits of radius to treat as fraction

    image = image.mul(mask);

    // (AFTER MOD) show the image inside the window
    cv::imshow(windowName, image);

    // wait for any keystroke
    cv::waitKey(0);

    // destroy the created window
    cv::destroyWindow(windowName);

    return 0;
}
