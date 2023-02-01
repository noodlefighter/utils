cmake_minimum_required(VERSION 3.16)
project(ebsx-main VERSION 1.0.0)

message("PKG_CONFIG_PATH:${PKG_CONFIG_PATH}")

string(TIMESTAMP COMPILE_TIME %Y%m%d_%H%M%S)
message("COMPILE_TIME:${COMPILE_TIME}")

set(CGAME_TARGET_LOGGER OFF CACHE BOOL "OFF CGAME_STDOUT_LOGGER" FORCE)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wall -fvisibility=hidden -Wno-unused-variable -Wno-unused-but-set-variable")

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Choose the type of build, options are: Debug Release RelWithDebInfo MinSizeRel." FORCE)
endif()



option(EBSX_EXAMPLES "Configure CMake to build examples (or not)" ON)
option(EBSX_USE_SDL2_VIDEO "Configure CMake to use sdl2_video (or not)" OFF)
option(EBSX_USE_VNCSERVER "Configure CMake to use libvncserver (or not)" ON)

set(MAIN_ROOT_PATH ${CMAKE_CURRENT_LIST_DIR})

set(GDMAIN-IOT_EXAMPLES OFF)

configure_file(${MAIN_ROOT_PATH}/include/ebsx_config.h.in ${MAIN_ROOT_PATH}/include/ebsx_config.h)




add_subdirectory(${MAIN_ROOT_PATH}/lib/gdmain-iot EXCLUDE_FROM_ALL)
add_subdirectory(${MAIN_ROOT_PATH}/lib/l8w8jwt EXCLUDE_FROM_ALL)
add_subdirectory(${MAIN_ROOT_PATH}/lib/GmSSL EXCLUDE_FROM_ALL)

include_directories(${MAIN_ROOT_PATH}/include
 ${MAIN_ROOT_PATH}/src
 ${MAIN_ROOT_PATH}/lib/gdmain-iot/include
 ${MAIN_ROOT_PATH}/lib/gdmain-iot/src
 ${MAIN_ROOT_PATH}/lib/gdmain-iot/lib/rapidyaml/src
 ${MAIN_ROOT_PATH}/lib/gdmain-iot/lib/rapidyaml/ext/c4core/src
 ${MAIN_ROOT_PATH}/lib/GmSSL/include
 ${MAIN_ROOT_PATH}/lib/l8w8jwt/include)


message(STATUS "${PROJECT_BINARY_DIR}")


add_subdirectory(${MAIN_ROOT_PATH}/src)

if(EBSX_EXAMPLES)
  add_subdirectory(${MAIN_ROOT_PATH}/example)
endif()

