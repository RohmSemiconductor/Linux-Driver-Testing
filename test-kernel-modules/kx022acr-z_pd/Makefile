obj-m += kx022_acr_z_test.o

all: kx022_acr_z_test dtb
kx022_acr_z_test: kx022_acr_z_test.c
	make -C ${KERNEL_DIR} CROSS_COMPILE=${CC} ARCH=arm M=$(PWD) modules
dtb: ${DTS_FILE}
	dtc -O dtb -o kx022_acr_z_test.dtbo -b 0 -@ ${DTS_FILE}

clean:
	rm -rf bd71828_test.dtbo
install:
	cp kx022_acr_z_test.dtbo  ${CFG_BBB_NFS_ROOT}/.
	cp kx022_acr_z_test.ko  ${CFG_BBB_NFS_ROOT}/.

debug_cfg:
	make -C ${KERNEL_DIR} CROSS_COMPILE=${CC} ARCH=arm M=$(PWD) CONFIG_DEBUG_SECTION_MISMATCH=y modules
