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
    
kernel_modules['dt_overlays']={
'bd71815':['bd71815_test.dtbo'],
'bd71828':['bd71828_test.dtbo'],#not yet installed
'bd71837':['bd71837_test.dtbo','bbb_only_I2C_1.dtbo' ],
'bd71847':['bd71847_test.dtbo'],
'bd9576':['bd9576_test.dtbo'],
}
kernel_modules['test']={
'bd71815':['bd71815_test.dtbo','bd71815-test.ko','bd71815-gpio-test.ko','bd71815-clktest.ko'],
'bd71828':['bd71828_test.dtbo','bd71828-test.ko','bd71828-gpio-test.ko','bd71828-clktest.ko'],#not yet installed
'bd71837':['bd71837_test.dtbo','bd71837-test.ko'], #,'bbb_only_I2C_1.dtbo'
'bd71847':['bd71847_test.dtbo','bd71847-test.ko','bd71847-test2.ko'],
'bd9576':['bd9576_test.dtbo','bd9576-test.ko'],
}

#Used for assert: test_merge_dt_overlay.py, output of lsmod
kernel_modules['merged_dt_overlay']={
'bd71815':['rohm_bd71828','gpio_bd71815','clk_bd718x7','bd71815_regulator','rtc_bd70528'], #lsmod OK(?)
'bd71828':['rohm_bd71828','gpio-bd71828','clk_bd718x7','bd71828_regulator','rtc_bd70528'], #lsmod OK(?) #not yet installed
'bd71837':['bd718x7_regulator','rohm_regulator','clk_bd718x7','rohm_bd718x7'], #lsmod OK
'bd71847':['bd718x7_regulator','rohm_regulator','clk_bd718x7','rohm_bd718x7'], #lsmod OK
'bd9576':['bd9576_test.dtbo','bd9576-test.ko'],
}

#Used for assert: test_insmod_tests.py, output of lsmod
kernel_modules['insmod_tests']={
'bd71815':['bd71815_test','bd71815_gpio_test','bd71815_clktest'], #lsmod OK
'bd71828':['bd71828_test.dtbo','bd71828-test.ko','bd71828-gpio-test.ko','bd71828-clktest.ko'],#not yet installed
'bd71837':['bd71837_test'], #lsmod OK
'bd71847':['bd71845_test','bd71847_test2'], #lsmod OK
'bd9576':['bd9576_test'], #lsmod OK
}

#useless
kernel_modules['init_regulator_test']={ #useless
'bd71815':['ti_am335x_tscadc','industrilio','kfifo_buf','ti_am335x_adc'],
'bd71828':['bd71828_test.dtbo','bd71828-test.ko','bd71828-gpio-test.ko','bd71828-clktest.ko'],#not yet installed
'bd71837':['bd71837_test.dtbo','bd71837-test.ko'], #,'bbb_only_I2C_1.dtbo'
'bd71847':['bd718x7_regulator','gpio_keys','rohm_regulator','clk_bd718x7','rohm_bd718x7'],
'bd9576':['bd9576_test.dtbo','bd9576-test.ko'],
}
#mva_overlay = mva_overlay | lsmod
