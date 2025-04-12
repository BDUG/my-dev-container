cmake_minimum_required(VERSION 3.15)
project(MyProject)

include_directories(include)
find_package(ZLIB REQUIRED)

message("Building with CMake version: ${CMAKE_VERSION}")

add_executable(test003
    src/test003.cpp
)
target_link_libraries(test003 ZLIB::ZLIB)

