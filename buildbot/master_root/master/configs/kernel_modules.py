###### test-kernel

kernel_modules={}

kernel_modules['linux_ver']={
'bd71815':['5.13'],
'bd71828':['5.6'], #bd71849 is similar
'bd71837':['4.20'],
'bd71847':['4.20'],
'bd9576':['5.13'],
#'bd99954':['5.'],
}

kernel_modules['build']={
'overlay_merger':['mva_overlay.ko'],
'bd71815':['bd71815_test.dtbo','bd71815-test.ko','bd71815-gpio-test.ko','bd71815-clktest.ko'],
'bd71828':['bd71828_test.dtbo','bd71828-test.ko','bd71828-gpio-test.ko','bd71828-clktest.ko'],
'bd71837':['bd71837_test.dtbo','bd71837-test.ko','bbb_only_I2C_1.dtbo'],
'bd71847':['bd71847_test.dtbo','bd71847-test.ko','bd71847-test2.ko'],
'bd9576':['bd9576_test.dtbo','bd9576-test.ko'],
'bd99954':['bd99954_test.dtbo'],
}
kernel_modules['dts_tests']={
        'bd71847':['ramprate2'],
        'bd9576':['ovd_uvd_disable'],
        'bd71815':['ramprate2']
        }

kernel_modules['dts_files']={
    'bd71847':{
#        'default':      'bd71847_test_outofrange.dts',
        'default':      'bd71847_test_oor_rampr1.dts',
#        'outofrange':   'bd71847_test_outofrange.dts',
#        'ramprate2':    'bd71847_test_ramprate2.dts',
            },
    'bd71837':{
        'default':      'bd71837_test_outofrange.dts',
#        'outofrange':   'bd71837_test_outofrange.dts',
        },
    'bd9576':{
        'default':      'bd9576-demo.dts'
        },
    'bd71815':{
        'default':      'bd71815_test_outofrange.dts',
        },
}

kernel_modules['dt_overlays']={
'bd71815':['bd71815_test.dtbo'],
'bd71828':['bd71828_test.dtbo'],#not yet installed
'bd71837':['bd71837_test.dtbo','bbb_only_I2C_1.dtbo'],
'bd71847':['bd71847_test.dtbo'],
'bd9576':['bd9576_test.dtbo']
}

kernel_modules['test']={
'bd71815':['bd71815-test.ko','bd71815-gpio-test.ko','bd71815-clktest.ko'],
'bd71828':['bd71828-test.ko','bd71828-gpio-test.ko','bd71828-clktest.ko'],
'bd71837':['bd71837-test.ko'],
'bd71847':['bd71847-test.ko','bd71847-test2.ko'],
'bd9576':['bd9576-test.ko']
}

#Used for assert: test_merge_dt_overlay.py, output of lsmod
kernel_modules['merged_dt_overlay']={
'bd71815':['rohm_bd71828','gpio_bd71815','clk_bd718x7','bd71815_regulator','rtc_bd70528'],
'bd71828':['rohm_bd71828','gpio_bd71828','clk_bd718x7','bd71828_regulator','rtc_bd70528'],
'bd71837':['bd718x7_regulator','rohm_regulator','clk_bd718x7','rohm_bd718x7'],
'bd71847':['bd718x7_regulator','rohm_regulator','clk_bd718x7','rohm_bd718x7'],
'bd9576':['bd9576_wdt','bd9576_regulator','rohm_bd9576'],
'bd96801':['bd96801_wdt','bd96801_regulator','rohm_bd96801']
}

#Used for assert: test_insmod_tests.py, output of lsmod
kernel_modules['insmod_tests']={
'bd71815':['bd71815_test','bd71815_gpio_test','bd71815_clktest'],
'bd71828':['bd71828_test','bd71828_gpio_test','bd71828_clktest'],
'bd71837':['bd71837_test'],
'bd71847':['bd71847_test','bd71847_test2'],
'bd9576':['bd9576_test'],
'bd96801':['bd96801_test'],
}

#useless
kernel_modules['init_regulator_test']={ #useless
'bd71815':['ti_am335x_tscadc','industrilio','kfifo_buf','ti_am335x_adc'],
'bd71828':['bd71828_test.dtbo','bd71828-test.ko','bd71828-gpio-test.ko','bd71828-clktest.ko'],
'bd71837':['bd71837_test.dtbo','bd71837-test.ko'], #,'bbb_only_I2C_1.dtbo'
'bd71847':['bd718x7_regulator','gpio_keys','rohm_regulator','clk_bd718x7','rohm_bd718x7'],
'bd9576':['bd9576_test.dtbo','bd9576-test.ko'],
}
