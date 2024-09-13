obj-m += bd96801-test.o

all: bd96801-test dtb
bd96801-test: bd96801-test.c
	make -C ${KERNEL_DIR} CROSS_COMPILE=${CC} ARCH=arm M=$(PWD) modules
dtb: ${DTS_FILE}
	dtc -O dtb -o bd96801_test.dtbo -b 0 -@ ${DTS_FILE}
clean:
	make -C ${KERNEL_DIR} CROSS_COMPILE=${CC} ARCH=arm M=$(PWD) clean
