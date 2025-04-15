COMPONENT=$(shell basename $(CURDIR))

#obj-m += $(COMPONENT)-test.o

#all: $(COMPONENT)-test dtb
all: dtb
#$(COMPONENT)-test: $(COMPONENT)-test.c $(COMPONENT)-gpio-test.c $(COMPONENT)-clktest.c
#	make -C ${KERNEL_DIR} CROSS_COMPILE=${CC} ARCH=arm M=$(PWD) modules
dtb: $(COMPONENT)_test.dts
	echo component is $(COMPONENT)
	./makedtb -i $(COMPONENT)_test.dts
	#dtc -O dtb -o $(COMPONENT)_test.dtbo -b 0 -@ $(COMPONENT)_test.dts

clean:
	rm -rf $(COMPONENT)_test.dtbo bd $(COMPONENT)-test.ko
install:
	#cp $(COMPONENT)_test.dtbo /home/mvaittin/nfs/.
	cp output/$(COMPONENT)_test.dtbo /home/mvaittin/nfs/.
#	cp $(COMPONENT)-test.ko /home/mvaittin/nfs/.
#	cp $(COMPONENT)-gpio-test.ko /home/mvaittin/nfs/.
#	cp $(COMPONENT)-clktest.ko /home/mvaittin/nfs/.

#debug_cfg:
#	make -C ${KERNEL_DIR} CROSS_COMPILE=${CC} ARCH=arm M=$(PWD) CONFIG_DEBUG_SECTION_MISMATCH=y modules
