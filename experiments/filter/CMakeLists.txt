cmake_minimum_required(VERSION 2.8)

project( filters_test )

find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )

add_executable( filters_test filters_test.cpp )

target_link_libraries( filters_test ${OpenCV_LIBS})