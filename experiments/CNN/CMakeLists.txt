cmake_minimum_required(VERSION 2.8)

project( cnn )

find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )

add_executable( cnn cnn.cpp )

target_link_libraries( cnn ${OpenCV_LIBS})