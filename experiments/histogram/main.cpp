#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <stdio.h>

using namespace std;
using namespace cv;

/**
 * @function main
 */
int main( int argc, char** argv )
{
    std::string img_path;

    // check for failure
    if(argc < 2){
        img_path = "../crap/test3.jpg";
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

    // try to create mask --------------------------------------------------------------
    cv::Mat mask = cv::Mat::zeros(image.rows, image.cols, CV_8U); // all 0

    std::vector<cv::Point> points;
    points.push_back(cv::Point(520 , 470));   //point1
    points.push_back(cv::Point(800 , 470));   //point2
    points.push_back(cv::Point(1120, 665));   //point3
    points.push_back(cv::Point(200 , 665));   //point4

    cv::fillConvexPoly(mask,              // Image to be drawn on
                       points,            // C-Style array of points
                       1, // Color , BGR form
                       CV_AA,             // connectedness, 4 or 8
                       0);                // Bits of radius to treat as fraction
    // ---------------------------------------------------------------------------------

    Mat dst;

    /// Separate the image in 3 places ( B, G and R )
    vector<Mat> bgr_planes;
    split( image, bgr_planes );

    /// Establish the number of bins
    int histSize = 256;

    /// Set the ranges ( for B,G,R )
    float range[] = { 0, 256 } ;
    const float* histRange = { range };

    Mat b_hist, g_hist, r_hist;

    /// Compute the histograms:
    calcHist( &bgr_planes[0], 1, 0, mask, b_hist, 1, &histSize, &histRange, true, false );
    calcHist( &bgr_planes[1], 1, 0, mask, g_hist, 1, &histSize, &histRange, true, false );
    calcHist( &bgr_planes[2], 1, 0, mask, r_hist, 1, &histSize, &histRange, true, false );

    printf("fack cols: %d | rows: %d\n", b_hist.cols, b_hist.rows);

    // Draw the histograms for B, G and R
    int hist_h = 400;
    int hist_w = histSize; //512;
    int unit_w = cvRound( (double) hist_w/histSize );

    Mat histImage( hist_h, hist_w, CV_8UC3, Scalar( 0,0,0) );

    /// Normalize the result to [ 0, histImage.rows ]
    normalize(b_hist, b_hist, 0, histImage.rows, NORM_MINMAX, -1, Mat() );
    normalize(g_hist, g_hist, 0, histImage.rows, NORM_MINMAX, -1, Mat() );
    normalize(r_hist, r_hist, 0, histImage.rows, NORM_MINMAX, -1, Mat() );

    /// Draw for each channel
    for( int i = 1; i < histSize; i++ )
    {
        line( histImage, Point( unit_w*(i-1), cvRound(b_hist.at<float>(i-1)) ) ,
                         Point( unit_w*(i)  , cvRound(b_hist.at<float>(i))   ) ,
                         Scalar( 255, 0, 0), 1, 8, 0  );
        line( histImage, Point( unit_w*(i-1), cvRound(g_hist.at<float>(i-1)) ) ,
                         Point( unit_w*(i)  , cvRound(g_hist.at<float>(i))   ) ,
                         Scalar( 0, 255, 0), 1, 8, 0  );
        line( histImage, Point( unit_w*(i-1), cvRound(r_hist.at<float>(i-1)) ) ,
                         Point( unit_w*(i)  , cvRound(r_hist.at<float>(i))   ) ,
                         Scalar( 0, 0, 255), 1, 8, 0  );
        //line( histImage, Point( bin_w*(i-1), hist_h - cvRound(g_hist.at<float>(i-1)) ) ,
        //        Point( bin_w*(i), hist_h - cvRound(g_hist.at<float>(i)) ),
        //        Scalar( 0, 255, 0), 2, 8, 0  );
        //line( histImage, Point( bin_w*(i-1), hist_h - cvRound(r_hist.at<float>(i-1)) ) ,
        //        Point( bin_w*(i), hist_h - cvRound(r_hist.at<float>(i)) ),
        //        Scalar( 0, 0, 255), 2, 8, 0  );
    }

    /// Display
    namedWindow("calcHist Demo", CV_WINDOW_AUTOSIZE );
    imshow("calcHist Demo", histImage );

    waitKey(0);

    return 0;
}
