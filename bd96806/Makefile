obj-m += bd96806-test.o

all: bd96806-test
bd96806-test: bd96806-test.c
	make -C ${KERNEL_DIR} CROSS_COMPILE=${CC} ARCH=arm M=$(PWD) modules
clean:
	make -C ${KERNEL_DIR} CROSS_COMPILE=${CC} ARCH=arm M=$(PWD) clean
