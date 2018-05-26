cmake_minimum_required(VERSION 2.8)

project( segmentation )

find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )

add_executable( segmentation segmentation.cpp )

target_link_libraries( segmentation ${OpenCV_LIBS})