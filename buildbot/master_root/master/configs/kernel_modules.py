###### test-kernel

kernel_modules={}

kernel_modules['build']={
'overlay_merger':['mva_overlay.ko'],
'bd71815':['bd71815_test.dtbo','bd71815-test.ko','bd71815-gpio-test.ko','bd71815-clktest.ko'],
'bd71828':['bd71828_test.dtbo','bd71828-test.ko','bd71828-gpio-test.ko','bd71828-clktest.ko'],
'bd71837':['bd71837_test.dtbo','bd71837-test.ko','bbb_only_I2C_1.dtbo'],
'bd71847':['bd71847_test.dtbo','bd71847-test.ko','bd71847-test2.ko'],
'bd9576':['bd9576_test.dtbo','bd9576-test.ko'],
'bd99954':['bd99954_test.dtbo'],
}
    
kernel_modules['test']={
'bd71815':['bd71815_test.dtbo','bd71815-test.ko','bd71815-gpio-test.ko','bd71815-clktest.ko'],
'bd71828':['bd71828_test.dtbo','bd71828-test.ko','bd71828-gpio-test.ko','bd71828-clktest.ko'],
'bd71837':['bd71837_test.dtbo','bd71837-test.ko','bbb_only_I2C_1.dtbo'],
'bd71847':['bd71847_test.dtbo','bd71847-test.ko','bd71847-test2.ko'],
'bd9576':['bd9576_test.dtbo','bd9576-test.ko'],
}


