#!/bin/bash
### Basic command to build a test kernel module

#export KERNEL_DIR=~/gits/linux CC=~/Linux-Driver-Testing/compilers/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf- PWD=~/test-kernel-modules/Linux-Driver-Testing/overlay_merger/ ; make

#dtc -@ -I dts -O dtb -o kx022a_i2c.dtbo kx022a_i2c.dts

### Kernel it self:
#cp accel_meter_config_v6.12-rc1 linux/.config
cp IIO_BUFFER_CB.config linux/.config

cd linux/
make -j8 ARCH=arm CROSS_COMPILE=/home/kale/Linux-Driver-Testing/compilers/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf- LOADADDR=0x80008000 olddefconfig

ccache make -j8 ARCH=arm CROSS_COMPILE=/home/kale/Linux-Driver-Testing/compilers/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf- LOADADDR=0x80008000

sudo make -j8 ARCH=arm CROSS_COMPILE=/home/kale/Linux-Driver-Testing/compilers/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf- LOADADDR=0x80008000 INSTALL_MOD_PATH=~/nfs/ modules_install

### BeagleBone dtb:
dtc -@ -I dts -O dtb -o arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb arch/arm/boot/dts/ti/omap/.am335x-boneblack.dtb.dts.tmp
### iio c file:
cd tools/iio/

make ARCH=arm CROSS_COMPILE=/home/kale/Linux-Driver-Testing/compilers/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf- LOADADDR=0x80008000
#make -j8 ARCH=arm CROSS_COMPILE=~/Linux-Driver-Testing/compilers/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf- LOADADDR=0x80008000 iio


