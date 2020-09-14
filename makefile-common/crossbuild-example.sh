#!/bin/bash

cd "$(dirname "$0")"

SDK=/home/mpc/workspaces/build/sk02/host
TCHAIN=$SDK/bin/arm-himix100-linux-
SYSROOT=$SDK/arm-buildroot-linux-uclibcgnueabi/sysroot
PKG_CONFIG_SYSROOT_DIR=$SYSROOT
PKG_CONFIG_PATH=$SYSROOT/usr/lib/pkgconfig

echo crossbuild script running...
echo SDK=$SDK
echo TCHAIN=$TCHAIN
echo SYSROOT=$SYSROOT
echo PKG_CONFIG_SYSROOT_DIR=$PKG_CONFIG_SYSROOT_DIR
echo PKG_CONFIG_PATH=$PKG_CONFIG_PATH

PKG_CONFIG_SYSROOT_DIR=$PKG_CONFIG_SYSROOT_DIR \
PKG_CONFIG_PATH=$PKG_CONFIG_PATH \
make TCHAIN=${TCHAIN} SYSROOT=${SYSROOT} $*
