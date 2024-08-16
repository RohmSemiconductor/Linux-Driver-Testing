#!/bin/bash
cd ~/Linux-Driver-Testing/buildbot/worker_root/worker1/Test_Linux/build/_test-kernel-modules/bd71828_pd_test

#cp ~/test-kernel-modules/$1/$2 .
#cp ~/test-kernel-modules/$1/$1_test.dts .

env KERNEL_DIR=../../ CC=/home/user01/Linux-Driver-Testing/compilers/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf- PWD=/home/user01/Linux-Driver-Testing/buildbot/worker_root/worker1/Test_Linux/build/_test-kernel-modules/bd71828_pd_test DTS_FILE=bd71828_pd_test_test.dts make
env CFG_BBB_NFS_ROOT=/home/user01/nfs make install
