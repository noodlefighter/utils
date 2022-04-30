#!/usr/bin/env bash

set -e

echo "deb http://mirrors.sjtug.sjtu.edu.cn/ubuntu/ xenial main restricted universe multiverse" > /etc/apt/sources.list
echo "deb http://mirrors.sjtug.sjtu.edu.cn/ubuntu/ xenial-updates main restricted universe multiverse" >> /etc/apt/sources.list
echo "deb http://mirrors.sjtug.sjtu.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse" >> /etc/apt/sources.list
echo "deb http://mirrors.sjtug.sjtu.edu.cn/ubuntu/ xenial-security main restricted universe multiverse" >> /etc/apt/sources.list

apt-get update
apt-get install -y build-essential wget python unzip rsync bc cpio lib32z1 lib32ncurses5 lib32stdc++6 \
                        u-boot-tools texinfo zlib1g-dev liblzo2-dev uuid-dev pkg-config libncurses-dev \
                        asciidoc binutils bzip2 gawk gettext git libncurses5-dev libz-dev patch zlib1g-dev \
                        lib32gcc1 libc6-dev-i386 subversion flex uglifyjs git-core gcc-multilib p7zip p7zip-full \
                        msmtp libssl-dev  libglib2.0-dev xmlto qemu-utils upx libelf-dev autoconf automake \
                        libtool autopoint device-tree-compiler g++-multilib antlr3 gperf \
                        git scons gcc-arm-none-eabi diffstat chrpath
apt-get clean
ln -sf bash /bin/sh
