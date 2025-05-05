###### test-kernel

kernel_modules={}

kernel_modules['linux_ver']={
'bd71815':['5.13'],
'bd71828':['5.6'], #bd71849 is similar
'bd71837':['4.20'],
'bd71847':['4.20'],
'bd9576':['5.13'],
'bd96801':['6.11'],
'kx022acr_z':['6.6'],
'kx132acr_lbz':['6.12'],
#'bd99954':['5.'],
'bd79703':['6.12']
}

kernel_modules['adc_pair']={
'bd79703':{
    'adc':'bd79124',
    'dtbo':'bd79124_test.dtbo',
    },
'bd79701':{
    'adc':'bd79104',
    'dtbo':'bd79104_test.dtbo',
    }
}

kernel_modules['build']={
'overlay_merger':['mva_overlay.ko'],
### PMICs
'bd71815':['bd71815_test.dtbo','bd71815-test.ko','bd71815-gpio-test.ko','bd71815-clktest.ko'],
'bd71828':['bd71828_test.dtbo','bd71828-test.ko','bd71828-gpio-test.ko','bd71828-clktest.ko'],
#'bd71837':['bd71837_test.dtbo','bd71837-test.ko','bbb_only_I2C_1.dtbo'],
'bd71837':['bd71837_test.dtbo','bd71837-test.ko'],
'bd71847':['bd71847_test.dtbo','bd71847-test.ko','bd71847-test2.ko'],
'bd9576':['bd9576_test.dtbo','bd9576-test.ko'],
'bd96801':['bd96801_test.dtbo','bd96801-test.ko'],
'bd99954':['bd99954_test.dtbo'],
### Sensors
'kx022acr_z':['kx022acr_z_test.dtbo', 'generic_accel_test.ko'],
'kx132acr_lbz':['kx132acr_lbz_test.dtbo', 'generic_accel_test.ko'],
### ADDAC
'bd79703':['bd79703_test.dtbo'],
'bd79701':['bd79701_test.dtbo'],
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
'bd9576':['bd9576_test.dtbo'],
'bd96801':['bd96801_test.dtbo'],
'kx022acr_z':['kx022acr_z_test.dtbo'],
'kx132acr_lbz':['kx132acr_lbz_test.dtbo'],
'bd79703':['chipselect_spi0.dtbo','bd79703_test.dtbo', kernel_modules['adc_pair']['bd79703']['dtbo']],
'bd79701':['chipselect_spi0.dtbo','bd79701_test.dtbo', kernel_modules['adc_pair']['bd79701']['dtbo']],
}

kernel_modules['test']={
'bd71815':['bd71815-test.ko','bd71815-gpio-test.ko','bd71815-clktest.ko'],
'bd71828':['bd71828-test.ko','bd71828-gpio-test.ko','bd71828-clktest.ko'],
'bd71837':['bd71837-test.ko'],
'bd71847':['bd71847-test.ko','bd71847-test2.ko'],
'bd9576':['bd9576-test.ko'],
'bd96801':['bd96801-test.ko'],
'kx022acr_z':['generic_accel_test.ko'],
'kx132acr_lbz':['generic_accel_test.ko'],
}

#Used for assert: test_merge_dt_overlay.py, output of lsmod
kernel_modules['merged_dt_overlay']={
'bd71815':['rohm_bd71828','gpio_bd71815','clk_bd718x7','bd71815_regulator','rtc_bd70528'],
#'bd71828':['rohm_bd71828','gpio_bd71828','clk_bd718x7','bd71828_regulator','rtc_bd70528'], #not yet installed
'bd71828':['rohm_bd71828'],
'bd71837':['bd718x7_regulator','rohm_regulator','clk_bd718x7','rohm_bd718x7'],
'bd71847':['bd718x7_regulator','rohm_regulator','clk_bd718x7','rohm_bd718x7'],
'bd9576':['bd9576_wdt','bd9576_regulator','rohm_bd9576'],
'bd96801':['bd96801_wdt', 'bd96801_regulator', 'rohm_bd96801'],
'kx022acr_z':['kionix_kx022a_spi', 'kionix_kx022a_i2c', 'kionix_kx022a'],
'kx132acr_lbz':['kionix_kx022a_spi', 'kionix_kx022a_i2c', 'kionix_kx022a'],
'bd79703':['industrialio', 'rohm_bd79703', 'rohm_bd79124', 'industrialio_adc'],
'bd79701':['industrialio', 'rohm_bd79703'],
'bd79124':['rohm_bd79124', 'industrialio_adc'],
}

#Used for assert: test_insmod_tests.py, output of lsmod
kernel_modules['insmod_tests']={
'bd71815':['bd71815_test','bd71815_gpio_test','bd71815_clktest'],
'bd71828':['bd71828_test','bd71828_gpio_test','bd71828_clktest'],
'bd71837':['bd71837_test'],
'bd71847':['bd71847_test','bd71847_test2'],
'bd9576':['bd9576_test'],
'bd96801':['bd96801_test'],
'kx022acr_z':['generic_accel_test'],
'kx132acr_lbz':['generic_accel_test'],
}

#useless
kernel_modules['init_regulator_test']={ #useless
'bd71815':['ti_am335x_tscadc','industrilio','kfifo_buf','ti_am335x_adc'],
'bd71828':['bd71828_test.dtbo','bd71828-test.ko','bd71828-gpio-test.ko','bd71828-clktest.ko'],
'bd71837':['bd71837_test.dtbo','bd71837-test.ko'], #,'bbb_only_I2C_1.dtbo'
'bd71847':['bd718x7_regulator','gpio_keys','rohm_regulator','clk_bd718x7','rohm_bd718x7'],
'bd9576':['bd9576_test.dtbo','bd9576-test.ko'],
}

