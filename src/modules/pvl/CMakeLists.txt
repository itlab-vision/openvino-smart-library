cmake_minimum_required( VERSION 2.8 ) 

project (PVL_wrapper)

find_package( OpenCV REQUIRED )

include_directories( ${OpenCV_INCLUDE_DIRS} )

add_library(PVL_wrapper SHARED pvl.cpp pvl.hpp pvl.def)

target_link_libraries(PVL_wrapper ${OpenCV_LIBS})  