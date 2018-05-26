#include "histogram.hpp"

// calculates intesity histogram
cv::Mat histogram::intensity_histogram(
    cv::Mat image,
    cv::Mat mask,
    int histSize
){
    /// Set the ranges ( for B,G,R )
    float range[] = { 0, 256 } ;
    const float* histRange = { range };

    // prepare return
    cv::Mat histo;

    /// Compute the histograms:
    calcHist( &image, 1, 0, mask, histo, 1, &histSize, &histRange, true, false );

    return histo;
}

