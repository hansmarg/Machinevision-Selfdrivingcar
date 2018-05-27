#include "shapes.hpp"

// draws a polygon over the image
void shapes::draw_polygon(
       cv::Mat img,
       std::vector<cv::Point> corners,
       cv::Scalar color,
       int thickness,
       int type,
       int shift
){

    unsigned int s = corners.size();
    if(s < 2) return;

    cv::line(img, corners[s-1], corners[0], color, thickness, type, shift);

    unsigned int i;
    for(i=1; i<s; i++){
        cv::line(img, corners[i-1], corners[i], color, thickness, type, shift);
    }
}

// create points for a trapazoid
std::vector<cv::Point> shapes::trapazoid(
    int a,
    int b,
    int center,
    int height,
    int y
){
    std::vector<cv::Point> corners;
    corners.push_back(cv::Point(center - a, y));          // point1
    corners.push_back(cv::Point(center + a, y));          // point2
    corners.push_back(cv::Point(center + b, y + height)); // point3
    corners.push_back(cv::Point(center - b, y + height)); // point4
    return corners;
}

// create points for a rectangle
std::vector<cv::Point> shapes::rectangle( int height, int width ){
    std::vector<cv::Point> corners;
    corners.push_back(cv::Point(     0 ,      0 )); // point1
    corners.push_back(cv::Point( width ,      0 )); // point2
    corners.push_back(cv::Point( width , height )); // point3
    corners.push_back(cv::Point(     0 , height )); // point4
    return corners;
}

// create points for a rectangle
void shapes::plot(
    cv::Mat canvas,
    cv::Mat vals_org,
    cv::Scalar color,
    int thickness,
    int y_max
){
    // clone vals
    cv::Mat vals(vals_org);

    if(y_max > -1){
        //printf("y_max: %d\n", y_max);

        vals.at<float>(0) = y_max;
        for( int i = 1; i < vals.rows; i++ ){
            if(vals.at<float>(i) > y_max){
                vals.at<float>(i) = y_max;
            }
        }


        //float sushi = 0;
        //for( int i = 0; i < vals.rows; i++ ){
        //    printf("%d -> %f\n", i, vals.at<float>(i));
        //    //sushi += vals.at<float>(i);
        //}
        //printf("sushi: %f\n", sushi);
    }

    // prepare unit width for x-axis streching
    int unit_w = cvRound( (double) canvas.cols/vals.rows );

    // normalize values for y-axis stretching
    cv::normalize(vals, vals, 0, canvas.rows, cv::NORM_MINMAX, -1, cv::Mat() );

    for( int i = 2; i < vals.rows; i++ ){
        cv::line( canvas, cv::Point( unit_w*(i-1), canvas.rows - cvRound(vals.at<float>(i-1)) ) ,
                          cv::Point( unit_w*(i)  , canvas.rows - cvRound(vals.at<float>(i))   ) ,
                          color, thickness, 8, 0  );
    }

}
