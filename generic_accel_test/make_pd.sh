#!/bin/bash

env KERNEL_DIR=/home/kale/test-kernel-modules/linux CC=/home/kale/Linux-Driver-Testing/compilers/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf- PWD=/home/kale/test-kernel-modules/generic_accel_test DTS_FILE=kx022a_i2c.dts make
env CFG_BBB_NFS_ROOT=/home/kale/nfs make install
