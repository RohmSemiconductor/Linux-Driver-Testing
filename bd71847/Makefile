obj-m += bd71847-test.o
obj-m += bd71847-test2.o

all:
	make -C ${KERNEL_DIR} CROSS_COMPILE=${CC} ARCH=arm M=$(PWD) modules

clean:
	make -C ${KERNEL_DIR} CROSS_COMPILE=${CC} ARCH=arm M=$(PWD) clean

install:
	cp bd71847-test.ko  ${CFG_BBB_NFS_ROOT}/.
	cp bd71847-test2.ko  ${CFG_BBB_NFS_ROOT}/.
	cp bd71847_test.dtbo  ${CFG_BBB_NFS_ROOT}/.

debug_cfg:
	make -C ${KERNEL_DIR} CROSS_COMPILE=${CC} ARCH=arm M=$(PWD) CONFIG_DEBUG_SECTION_MISMATCH=y modules
