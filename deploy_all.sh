#!/bin/bash
./build_kernel.sh
./copy_kernel_binaries_tftp_nfs.sh
#./build_dts_tkm.sh
#./copy_dts_tkm_nfs.sh
cd linux/test-kernel-modules/kx022acr-z_pd/
./make_pd.sh
