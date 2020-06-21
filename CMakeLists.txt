cmake_minimum_required(VERSION 2.8.11)

project("fastddsgen")
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()



include(${PROJECT_SOURCE_DIR}/cmake/dev/java_support.cmake)

gradle_build(${PROJECT_SOURCE_DIR} ${PROJECT_NAME}genJar
    THIRDPARTY_DEPENDENCY idl-parser
    )

