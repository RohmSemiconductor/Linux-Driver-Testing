#!/bin/bash
### Basic command to build a test kernel module

### iio c file:
cd linux/tools/iio/

make ARCH=arm CROSS_COMPILE=/home/kale/Linux-Driver-Testing/compilers/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf- LOADADDR=0x80008000
#make -j8 ARCH=arm CROSS_COMPILE=~/Linux-Driver-Testing/compilers/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf- LOADADDR=0x80008000 iio

cp iio_generic_buffer /home/kale/nfs/

