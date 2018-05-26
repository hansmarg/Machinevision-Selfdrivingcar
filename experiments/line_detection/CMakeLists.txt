cmake_minimum_required(VERSION 2.8)

project( hough_test )

find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )

add_executable( hough_test hough_test.cpp )

target_link_libraries( hough_test ${OpenCV_LIBS})