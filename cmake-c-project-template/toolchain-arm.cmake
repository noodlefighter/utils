# refers:
# - https://gitlab.kitware.com/cmake/community/-/wikis/doc/cmake/CrossCompiling
# - https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html?highlight=cmake_c_compiler

SET(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR arm)

# rootfs
set(CMAKE_SYSROOT /opt/myir-imx-fb/4.1.15-2.0.1/sysroots/cortexa7hf-neon-poky-linux-gnueabi/)

# specify the cross compiler
SET(CMAKE_C_COMPILER   /opt/myir-imx-fb/4.1.15-2.0.1/sysroots/x86_64-pokysdk-linux/usr/bin/arm-poky-linux-gnueabi/arm-poky-linux-gnueabi-gcc)
SET(CMAKE_CXX_COMPILER /opt/myir-imx-fb/4.1.15-2.0.1/sysroots/x86_64-pokysdk-linux/usr/bin/arm-poky-linux-gnueabi/arm-poky-linux-gnueabi-g++)
set(CMAKE_C_FLAGS "-march=armv7ve -marm -mfpu=neon  -mfloat-abi=hard -mcpu=cortex-a7")
set(CMAKE_CXX_FLAGS "-march=armv7ve -marm -mfpu=neon  -mfloat-abi=hard -mcpu=cortex-a7")

# where is the target environment
SET(CMAKE_FIND_ROOT_PATH ${CMAKE_SYSROOT})

# search for programs in the build host directories (not necessary)
SET(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)

# for libraries and headers in the target directories
SET(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
SET(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

# pkgconfig
set(ENV{PKG_CONFIG_DIR} "")
set(ENV{PKG_CONFIG_LIBDIR} "${CMAKE_SYSROOT}/usr/lib/pkgconfig:${CMAKE_SYSROOT}/usr/share/pkgconfig")
set(ENV{PKG_CONFIG_SYSROOT_DIR} ${CMAKE_SYSROOT})
