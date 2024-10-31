#!/bin/bash
cd linux
make -j8 ARCH=arm CROSS_COMPILE=/home/kale/Linux-Driver-Testing/compilers/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf- LOADADDR=0x80008000 menuconfig
