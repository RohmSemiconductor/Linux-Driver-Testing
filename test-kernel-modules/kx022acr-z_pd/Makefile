obj-m += generic_accel_test.o

all: generic_accel_test dtb
generic_accel_test: accel_module_test.c
	make -C ${KERNEL_DIR} CROSS_COMPILE=${CC} ARCH=arm M=$(PWD) modules
dtb: ${DTS_FILE}
	dtc -O dtb -o ${TEST_TARGET}_test.dtbo -b 0 -@ ${DTS_FILE}

clean:
	rm -rf bd71828_test.dtbo
install:
	cp ${TEST_TARGET}_test.dtbo  ${CFG_BBB_NFS_ROOT}/.
	cp generic_accel_test.ko  ${CFG_BBB_NFS_ROOT}/.

debug_cfg:
	make -C ${KERNEL_DIR} CROSS_COMPILE=${CC} ARCH=arm M=$(PWD) CONFIG_DEBUG_SECTION_MISMATCH=y modules
