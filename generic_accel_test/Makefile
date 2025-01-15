obj-m += generic_accel_test.o

all: generic_accel_test
generic_accel_test: generic_accel_test.c
	make -C ${KERNEL_DIR} CROSS_COMPILE=${CC} ARCH=arm M=$(PWD) modules
clean:
	rm -rf bd71828_test.dtbo
install:
	cp ${TEST_TARGET}_test.dtbo  ${CFG_BBB_NFS_ROOT}/.
	cp generic_accel_test.ko  ${CFG_BBB_NFS_ROOT}/.

debug_cfg:
	make -C ${KERNEL_DIR} CROSS_COMPILE=${CC} ARCH=arm M=$(PWD) CONFIG_DEBUG_SECTION_MISMATCH=y modules
