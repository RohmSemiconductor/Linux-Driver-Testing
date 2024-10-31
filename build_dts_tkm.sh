#!/bin/bash
cd test-kernel-modules/
cd kx022acr-z/
dtc -@ -I dts -O dtb -o kx022a_i2c.dtbo kx022a_i2c.dts

cd ..
cd overlay_merger/
export KERNEL_DIR=/home/kale/codes/sensor_tests/linux CC=/home/kale/Linux-Driver-Testing/compilers/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf- PWD=/home/kale/codes/sensor_tests/test-kernel-modules/overlay_merger/ ; make
