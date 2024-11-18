#!/bin/bash

env KERNEL_DIR=/home/kale/codes/sensor_tests/linux CC=/home/kale/Linux-Driver-Testing/compilers/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf- PWD=/home/kale/codes/sensor_tests/test-kernel-modules/kx022acr-z_pd DTS_FILE=$1_test.dts TEST_TARGET=$1 make
env CFG_BBB_NFS_ROOT=/home/kale/nfs TEST_TARGET=$1 make install
