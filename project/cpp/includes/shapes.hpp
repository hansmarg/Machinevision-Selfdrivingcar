#ifndef _SHAPES_H_
#define _SHAPES_H_

#include <opencv2/opencv.hpp>
#include <iostream>

namespace shapes{
    void draw_polygon(
           cv::Mat img,
           std::vector<cv::Point> corners,
           cv::Scalar color = cv::Scalar(0,0,0),
           int thickness = 4,
           int type = 8,
           int shift = 0 );

    std::vector<cv::Point> trapazoid(
            int a,
            int b,
            int center,
            int height,
            int y );

    std::vector<cv::Point> rectangle(
            int height,
            int width );

    void plot(
            cv::Mat canvas,
            cv::Mat vals_org,
            cv::Scalar color = cv::Scalar(255,0,0),
            int thickness = 1,
            int y_max = -1);
}

#endif // _SHAPES_H_
