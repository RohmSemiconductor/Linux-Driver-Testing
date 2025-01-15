COMMON_NAME := bd9576-demo

#obj-m := ${COMMON_NAME}.o
obj-m := bd9576-test.o

all:
	make -C ${KERNEL_DIR} CROSS_COMPILE=${CC} ARCH=arm M=$(PWD) modules
clean:
	make -C ${KERNEL_DIR} CROSS_COMPILE=${CC} ARCH=arm M=$(PWD) clean
	rm -rf bd9576_test.dtbo
install:
	cp bd9576-test.ko ${CFG_BBB_NFS_ROOT}/.
	cp bd9576_test.dtbo ${CFG_BBB_NFS_ROOT}/.

debug_cfg:
	make -C ${KERNEL_DIR} CROSS_COMPILE=${CC} ARCH=arm M=$(PWD) CONFIG_DEBUG_SECTION_MISMATCH=y modules
