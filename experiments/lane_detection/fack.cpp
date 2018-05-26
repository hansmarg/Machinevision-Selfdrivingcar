    cv::Vec3b intensity;
    uint8_t blue;
    uint8_t green;
    uint8_t red ;
    int i, j;


    printf("BEFORE:\n");
    for(i=0; i<20; i++){
        for(j=0; j<20; j++){
            intensity = image.at<cv::Vec3b>(i, j);
            blue  = intensity.val[0];
            green = intensity.val[1];
            red   = intensity.val[2];
            printf("(%2.d, %2.d): blue: %d, green: %d, red: %d\n", i, j, blue, green, red);
        }
    }

    //image /= 64;
    //image *= 64;

    //int l = 220;
    //int h = 255;
    //cv::Mat after;
    //cv::Scalar min_color = cv::Scalar(l,l,l);
    //cv::Scalar max_color = cv::Scalar(h,h,h);
    //cv::inRange(image, min_color,  max_color, image);
