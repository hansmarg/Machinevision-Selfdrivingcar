cmake_minimum_required( VERSION 3.5.1 )

project(CarMachineVision)

# Compiler flags
if (MSVC)
  set(compiler_options /W4)
  add_definitions(/D_USE_MATH_DEFINES)
else ()
  set(compiler_options -Wall -Wextra -Wpedantic)
endif (MSVC)

# Find libraries
find_package(OpenCV 3.3.1 REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(sophus REQUIRED)
find_package(GeographicLib REQUIRED)

# lane detection program ----------------------------------------------------------------------
add_executable( lane
                lane.cpp
                includes/shapes.cpp
              )

target_link_libraries(lane ${OpenCV_LIBS} )
target_include_directories(lane SYSTEM PRIVATE ${sophus_INCLUDE_DIRS})
target_compile_options(lane PRIVATE ${compiler_options})
set_target_properties(lane PROPERTIES CXX_STANDARD_REQUIRED ON CXX_STANDARD 11)

# hisogram program ----------------------------------------------------------------------------
add_executable( histogram
                histogram.cpp
                includes/shapes.cpp
                includes/histogram.cpp
              )

target_link_libraries(histogram ${OpenCV_LIBS} )
target_include_directories(histogram SYSTEM PRIVATE ${sophus_INCLUDE_DIRS})
target_compile_options(histogram PRIVATE ${compiler_options})
set_target_properties(histogram PROPERTIES CXX_STANDARD_REQUIRED ON CXX_STANDARD 11)
