#include <opencv2/opencv.hpp>
#include <iostream>
#include <opencv2/imgproc/imgproc.hpp>

//#include "../filter/filters.cpp"
#include "../line_detection/hough_test.cpp"

using namespace cv;
using namespace std;

/*
double cv::kmeans 	( 	InputArray  	data,
		int  	K,
		InputOutputArray  	bestLabels,
		TermCriteria  	criteria,
		int  	attempts,
		int  	flags,
		OutputArray  	centers = noArray() 
	) 	
*/

Mat frame;
cv::Point2f pt(-1,-1);
bool newCoords = false;


void mouse_callback(int  event, int  x, int  y, int  flag, void *param)
{
    if (event == EVENT_LBUTTONDOWN)
    {
        // Store point coordinates
        pt.x = x;
        pt.y = y;
        newCoords = true;
    }
}

std::vector<cv::Point> create_rect()
{

	std::vector<cv::Point> square;

	square.push_back(pt.clone());
	newCoords = false;

	while(newCoords == false);

	square.push_back(pt.clone());
	newCoords = false;

	return square;
}

int main(int argc, char** argv)
{
	Mat	frame = imread( argv[1], IMREAD_COLOR ); // Read image
    Mat edges;
    namedWindow("img", 1);

    // Set callback
    setMouseCallback("img", mouse_callback);

    for (;;)
    {
        
		

        // Exit if 'q' is pressed
        if ((waitKey(1) & 0xFF) == 'q') break;
    }
    // the camera will be deinitialized automatically in VideoCapture destructor
    return 0;
}
/*
int main(int argc, char** argv){

	cv::Mat frame;

	frame = imread( argv[1], IMREAD_COLOR ); // Read image




	showim("Frame end", frame);
	return 0; 
}
*/