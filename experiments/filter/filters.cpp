#include <stdio.h>
#include <iostream>
#include <fstream> 
#include <opencv2/opencv.hpp>
#include <vector>
#include <iterator>

using namespace std;
using namespace cv;

int DEFAULT_PYR_DEPTH = 3;

Mat sobel_func(cv::Mat img) {
	
	Mat frame, frame_gray;
	Mat ret;

	int scale = 1;
	int delta = 0;
	int ddepth = CV_16S;

	frame = img.clone();
	
	if(frame.empty()){ 

		throw std::invalid_argument( "Frame is empty" );
		//return -1; 
	}
	
	//GaussianBlur( frame, frame, Size(3,3), 0, 0, BORDER_DEFAULT );	// Removes noise with Gaussian blur
	GaussianBlur( frame, frame, Size(7,7), 2, 2, BORDER_DEFAULT );
	
	cvtColor( frame, frame_gray, COLOR_BGR2GRAY );	// Converts to grayscale
	
	Mat grad_x, grad_y;
	Mat abs_grad_x, abs_grad_y;
	
	Sobel( frame_gray, grad_x, ddepth, 1, 0, 3, scale, delta, BORDER_DEFAULT );	// Calculates Sobel derivatives
	Sobel( frame_gray, grad_y, ddepth, 0, 1, 3, scale, delta, BORDER_DEFAULT );	// 

	convertScaleAbs( grad_x, abs_grad_x );	// Converts to absolute values
	convertScaleAbs( grad_y, abs_grad_y );	//

	addWeighted( abs_grad_x, 0.5, abs_grad_y, 0.5, 0, ret );	// Sums the derivatives

	return ret;
}
	//Scharr( frame_gray, grad_x, ddepth, 1, 0, scale, delta, BORDER_DEFAULT );	// Mulig en raskere sobel
	//Scharr( frame_gray, grad_y, ddepth, 0, 1, scale, delta, BORDER_DEFAULT );	//


// Returns a gaussian pyramid for a given frame.
std::vector<cv::Mat> gaussian_pyramid(cv::Mat img, int size = DEFAULT_PYR_DEPTH) {
	
	std::vector<cv::Mat> G;

	cv::Mat src = img;
	cv::Mat dst;


	for (int i = 0; i < size; i++)
	{
		pyrDown(src, src);		// blurs and downscales

		G.push_back(src);	// Appends to the L
	}

	return G;	
}

// Returns the Laplacian pyramid of a given image.
std::vector<cv::Mat> laplacian_pyramid(cv::Mat img, std::vector<cv::Mat> G = std::vector<cv::Mat>(), int size = DEFAULT_PYR_DEPTH) {

	std::vector<cv::Mat> L;

	cv::Mat src = img;
	cv::Mat G_up;

	if(G.empty()) {
		G = gaussian_pyramid(img, size);
	}
	
	size = G.size();
	
	L = G;

	for (int i = 0; i < size - 1; ++i)
	{
		pyrUp(G[i+1], G_up);

		L[i] = L[i] - G_up;
	}

	return L;
}

