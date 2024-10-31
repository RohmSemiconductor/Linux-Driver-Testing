#!/bin/bash
### Basic command to build a test kernel module

#export KERNEL_DIR=~/gits/linux CC=~/Linux-Driver-Testing/compilers/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf- PWD=~/test-kernel-modules/Linux-Driver-Testing/overlay_merger/ ; make

#dtc -@ -I dts -O dtb -o kx022a_i2c.dtbo kx022a_i2c.dts

### BeagleBone dtb:
#dtc -@ -I dts -O dtb -o arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb arch/arm/boot/dts/ti/omap/.am335x-boneblack.dtb.dts.tmp
### iio c file:
cp linux/arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb /var/lib/tftpboot
cp linux/arch/arm/boot/zImage /var/lib/tftpboot
cp linux/tools/iio/iio_generic_buffer /home/kale/nfs/
#make -j8 ARCH=arm CROSS_COMPILE=~/Linux-Driver-Testing/compilers/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf- LOADADDR=0x80008000 iio


