import operator
import pytest

result = {
    'type' :    None,
    'stage' :   None,
    'product':  None,
    'expect':   [],
    'return':   [],
    'lsmod':    [],
    'debug':    None,
}

report_file_names = ['temp_results', 'summary']

def checkStdOut(stdout,checkString):
    if any(checkString in s for s in stdout):
        return 0

def checkStr(stdout,checkString):
    if checkString in stdout:
        return 0

def initialize_report(bb_project, linux_ver, revision):
    for report_file in report_file_names:
        report_file = open('./temp_results/'+report_file+'.txt', 'w+', encoding='utf-8')
        print("BuildBot project: "+bb_project+"\n", end='', file=report_file)
        print("Linux version: "+linux_ver+"\n", end='', file=report_file)
        print("Commit hash: "+revision+"\n\n", end='', file=report_file)
        report_file.close()

def initialize_product(type, product):
    for report_file in report_file_names:
        report_file = open('./temp_results/'+report_file+'.txt', 'a', encoding='utf-8')
        report_file.seek(0,2)
        print("Testing: "+product+" "+type+"\n", end='', file=report_file)
        report_file.close()

def finalize_product(product, do_steps):
    if do_steps == 'True':
        result = "PASSED"
    else:
        result = "FAILED"
    for report_file in report_file_names:
        report_file = open('./temp_results/'+report_file+'.txt', 'a', encoding='utf-8')
        report_file.seek(0,2)
        print("Test results: "+product+": "+result+"\n\n", end='', file=report_file)
        report_file.close()

def bisect_result(timestamped_dir,bb_project, final_output, bisect_state):
    report_file = open('./'+timestamped_dir+'_'+bb_project+'/summary.txt', 'a', encoding='utf-8')
    report_file.seek(0,2)
    print("Git bisect state: "+bisect_state+"\n", end='', file=report_file)
    print(final_output+"\n", end='', file=report_file)
    report_file.close()

def kernel_error_report(stderr):
    report_file = open('./temp_results/summary.txt', 'a', encoding='utf-8')
    report_file.seek(0,2)
    print("Building kernel failed!\nstderr:\n\n", end='', file=report_file)
    print(stderr+'\n', end='', file=report_file)
    report_file.close()

def overlay_merger_error_report(stderr):
    report_file = open('./temp_results/summary.txt', 'a', encoding='utf-8')
    report_file.seek(0,2)
    print("Building overlay merger failed!\nstderr:\n\n", end='', file=report_file)
    print(stderr+'\n', end='', file=report_file)
    report_file.close()

def dts_error_report(product, dts, stdout):
    report_file = open('./temp_results/temp_results.txt', 'a', encoding='utf-8')
    summary = open('./temp_results/summary.txt', 'a', encoding='utf-8')
    report_file.seek(0,2)
    summary.seek(0,2)
    print(product+": dts build failed: dts: "+dts+"\n", end='', file=report_file)
    print(stdout+'\n', end='', file=report_file)
    print(product+": dts build failed: dts: "+dts+"\n", end='', file=summary)
    report_file.close()

def report_dmesg(product, stdout):
    report_file = open('../temp_results/'+product+'/dmesg.txt', 'w+', encoding='utf-8')
    print(type(stdout))
    print(len(stdout))
    x = 0
    for line in stdout:
        print(stdout[x]+'\n', end='',file=report_file)
        x = x+1
    report_file.close()

def to_str(result):
    if type(result) != str:
        result = str(result)
    return result

def _print_lsmod(result, report_file):
    print("---- LSMOD ----\n", end='', file=report_file)
    for line in result['lsmod']:
        print(line+"\n", end='', file=report_file)
    print("---- /LSMOD ----\n", end='', file=report_file)

### Use this at the end of _assert_* functions so the same
### assert and report_file.close do not have to be used always
def _assert_test(result, report_file, summary):
    report_file.close()
    summary.close()
    if result['expect'] == 'range':
        if type(result['return']) is list:
            x=0
            for return_value in result['return']:
                if type(result['expect_high']) is list:
                    assert return_value <= result['expect_high'][x] and return_value >= result['expect_low'][x]
                else:
                    assert return_value <= result['expect_high'] and return_value >= result['expect_low']
                x=x+1
        else:
            assert result['return'] <= result['expect_high'] and result['return'] >= result['expect_low']
    else:
        assert result['expect'] == result['return']

#### Generic steps
def _assert_generic_kunit_test(result, report_file, summary):
    if result['expect'] == result['return']:
        print( "Kunit test result: "+result['substage']+": PASSED\n\n", end='', file=summary)

    else:
        kunit_file = open('../temp_results/kunit_'+result['substage']+'_result.txt', 'w+', encoding='utf-8')
        kunit_full_dmesg = open('../temp_results/full_kunit_dmesg.txt', 'w+', encoding='utf-8')

        print( "Kunit test result: "+result['substage']+" FAILED: Found 'not ok' in the Kunit dmesg prints.\n\n", end='', file=summary)
        print( "Kunit test result: "+result['substage']+" FAILED: Found 'not ok' in the Kunit dmesg prints.\n\n", end='', file=kunit_file)

        x = 0
        for line in result['kunit_dmesg']:
            print(result['kunit_dmesg'][x]+'\n', end='', file=kunit_file)
            x = x+1

        kunit_file.close()

        x = 0
        for line in result['kunit_dmesg']:
            print(result['kunit_dmesg'][x]+'\n', end='', file=kunit_full_dmesg)
            x = x+1

        kunit_full_dmesg.close()

    _assert_test(result, report_file, summary)

def _assert_generic_get_dmesg(result, report_file, summary):
    if result['expect'] != result['return']:
        print( "Getting dmesg failed! Returncode: Received: "+str(result['return'])+", Expected: "+str(result['expect'])+"\n", end='', file=report_file)
        print( "Getting dmesg failed! Returncode: Received: "+str(result['return'])+", Expected: "+str(result['expect'])+"\n", end='', file=summary)
    _assert_test(result, report_file, summary)

def _assert_generic_merge_dt_overlay_insmod_tests(result, report_file, summary):
    if result['expect'] != result['return']:
        print( result['stage']+" failed: lsmod did not contain", end='', file=report_file)
        print( result['stage']+" failed\n", end='', file=summary)
        x = 0
        for i in result['expect']:
            if result['expect'][x][1] != result['return'][x][1]:
                print(" '"+result['expect'][x][0]+"'", end='', file=report_file)
            x = x+1
        print("\n", end='', file=report_file)
        _print_lsmod(result, report_file)
    _assert_test(result, report_file, summary)

def _assert_generic_init_overlay(result, report_file, summary):
    if result['expect'] != result['return']:
        print( "test_001_init_overlay failed: lsmod  did not contain 'mva_overlay'!\n", end='', file=report_file)
        print( "test_001_init_overlay failed: lsmod  did not contain 'mva_overlay'!\n", end='', file=summary)
        _print_lsmod(result, report_file)
    _assert_test(result, report_file, summary)

def _assert_generic_login(result, report_file, summary):
    if result['expect'] != result['return']:
        print( "Login failed: Power port "+result['expect'][0]+": "+result['expect'][1]+". Returncode: Received: "+str(result['return'][2])+", Expected: "+str(result['expect'][2])+"\n", end='', file=report_file)
        print( "Login failed: Power port "+result['expect'][0]+": "+result['expect'][1]+". Returncode: Received: "+str(result['return'][2])+", Expected: "+str(result['expect'][2])+"\n", end='', file=summary)

    _assert_test(result, report_file, summary)

def _assert_generic_ip_power(result, report_file, summary):
    if result['expect'] != result['return']:
        print( "Something wrong with controlling IP Power 9850: Received: "+str(result['return'])+", Expected: "+str(result['expect'])+". Check cable?\n", end='', file=report_file)
        print( "Something wrong with controlling IP Power 9850: Received: "+str(result['return'])+", Expected: "+str(result['expect'])+". Check cable?\n", end='', file=summary)

    _assert_test(result, report_file, summary)

def login_fail(power_port, beagle):
    report_file = open('../temp_results/temp_results.txt', 'a', encoding='utf-8')
    report_file.seek(0,2)
    print("Login failed: Power port:"+power_port+" BeagleBone: "+beagle+"\n\n", end='', file=report_file)
    report_file.close()

def init_overlay_fail():
    report_file = open('../temp_results/temp_results.txt', 'a', encoding='utf-8')
    report_file.seek(0,2)
    print("Installing overlay merger failed! This step is common to all PMICs.\n\n", end='', file=report_file)
    print("\n", end='', file=report_file)
    report_file.close()

def merge_dt_overlay_fail(product, dt_overlay):
    report_file = open('../temp_results/temp_results.txt', 'a', encoding='utf-8')
    report_file.seek(0,2)
    print(product, ": Merge device tree overlay failed: "+dt_overlay+" module missing (lsmod) \n\n", end='', file=report_file)
    report_file.close()

def insmod_fail(product, insmod):
    report_file = open('../temp_results/temp_results.txt', 'a', encoding='utf-8')
    report_file.seek(0,2)
    print(product, ": insmod failed: "+insmod+" module missing (lsmod) \n\n", end='', file=report_file)
    report_file.close()

def sanity_check_fail():
    pass

def generic_step_fail(tf, power_port=None, beagle=None, product=None,dt_overlay=None, insmod=None):
    report_file = open('../temp_results/temp_results.txt', 'a', encoding='utf-8')
    report_file.seek(0,2)
    if tf == "login":
        print("Login failed: Power port:"+power_port+" BeagleBone: "+beagle+"\n\n", end='', file=report_file)

    elif tf == "init_overlay":
        print("Installing overlay merger failed! This step is common to all PMICs.\n\n", end='', file=report_file)

    elif tf == "insmod":
        print(product, ": insmod failed: "+insmod+" module missing (lsmod) \n\n", end='', file=report_file)

    elif tf == "dt_overlay":
        print(product, ": Merge device tree overlay failed: "+dt_overlay+" module missing (lsmod) \n\n", end='', file=report_file)

    report_file.close()

### _assert functions for Sensors

def _assert_sensor_test_sampling_frequency_match_timestamp(result, report_file, summary):
    for x in range(len(result['return'])):
        if ((result['return'][x] <= result['expect_low']) or (result['return'][x] >= result['expect_high'])):
            print( "Sampling rate "+str(result['sampling_frequency'])+" Hz behaved unexpectedly: Time between timestamps:  Received: "+str(result['return'][x])+"ns, Expected: "+str(result['expect_perfect'])+"ns, Allowed range: "+str(result['expect_low'])+"ns - "+str(result['expect_high'])+"ns ("+str(result['tolerance'])+"% tolerance)\nDifference between received and expected: "+str(result['return_diff'][x])+"ns\n", end='', file=report_file)

            print( "Sampling rate "+str(result['sampling_frequency'])+" Hz behaved unexpectedly: Time between timestamps:  Received: "+str(result['return'][x])+"ns, Expected: "+str(result['expect_perfect'])+"ns, Allowed ("+str(result['tolerance'])+"% tolerance)\n", end='', file=summary)
    _assert_test(result, report_file, summary)

def _assert_sensor_test_gscale_raw_match(result, report_file, summary):
    for x in range(len(result['return'])):
        if ((result['return'][x] <= result['expect_low'][x]) or (result['return'][x] >= result['expect_high'][x])):
            print( "G scale +/- "+str(result['gscale'][x])+" Failed :in_accel_"+result['axis'][x]+"_raw returned: "+str(result['return'][x])+", Expected: "+str(result['expect_perfect'][x])+", Allowed range: "+str(result['expect_low'][x])+" - "+str(result['expect_high'][x])+" ("+str(result['tolerance'][x])+"G tolerance)\nDifference between received and expected: "+str(result['return_diff'][x])+"\n", end='', file=report_file)

            print( "G scale +/- "+str(result['gscale'][x])+" Failed :in_accel_"+result['axis'][x]+"_raw returned: "+str(result['return'][x])+", Expected: "+str(result['expect_perfect'][x])+", Allowed range: "+str(result['expect_low'][x])+" - "+str(result['expect_high'][x])+" ("+str(result['tolerance'][x])+"G tolerance)\n", end='', file=summary)

    _assert_test(result, report_file, summary)

def _assert_sensor_test_gsel(result, report_file, summary):
    if result['expect'] != result['return']:
        print( "Setting GSEL failed:  Received: "+str(result['return'])+", Expected: "+str(result['expect'])+"\n", end='', file=report_file)
        print( "Setting GSEL failed:  Received: "+str(result['return'])+", Expected: "+str(result['expect'])+"\n", end='', file=summary)

    _assert_test(result, report_file, summary)

### Assert functions for PMICs

def _assert_pmic_read_dt_setting(result, report_file, summary):
    if result['expect'] != result['return']:
        if result['expect'][1] == 'ramprate':
            if type(result['return'][2]) == float:
                result['return'][2] = int(result['return'][2])
            print( "Device tree setting failed (dts: '"+result['expect'][0]+"', setting: '"+result['expect'][1]+"'): Regulator "+result['regulator']+": Received: "+str(result['return'][2])+" uV/uS, Expected: "+str(result['expect'][2])+" uV/uS\n", end='', file=report_file)
            print( "Device tree setting failed (dts: '"+result['expect'][0]+"', setting: '"+result['expect'][1]+"'): Regulator "+result['regulator']+": Received: "+str(result['return'][2])+" uV/uS, Expected: "+str(result['expect'][2])+" uV/uS\n", end='', file=summary)

        if result['expect'][1] == 'ovd' or result['expect'][1] == 'uvd':
            if type(result['return'][2]) == float:
                result['return'][2] = int(result['return'][2])
            print( "Device tree setting failed (dts: '"+result['expect'][0]+"', setting: '"+result['expect'][1]+"'): Regulator "+result['regulator']+": Received: "+str(result['return'][2])+" mV or mA, Expected: "+str(result['expect'][2])+" mV or mA\n", end='', file=report_file)
            print( "Device tree setting failed (dts: '"+result['expect'][0]+"', setting: '"+result['expect'][1]+"'): Regulator "+result['regulator']+": Received: "+str(result['return'][2])+" mV or mA, Expected: "+str(result['expect'][2])+" mV or mA\n", end='', file=summary)

    _assert_test(result, report_file, summary)

def _assert_pmic_out_of_range_voltages(result, report_file, summary):
    if result['expect'] != result['return']:
        print( "Out of range test fail ("+result['expect'][0]+"): Regulator "+result['regulator']+" voltage changed: Received: "+str(result['return'][1])+", Expected: "+str(result['expect'][1])+"\n", end='', file=report_file)
        print( "Out of range test fail ("+result['expect'][0]+"): Regulator "+result['regulator']+" voltage changed: Received: "+str(result['return'][1])+", Expected: "+str(result['expect'][1])+"\n", end='', file=summary)

    _assert_test(result, report_file, summary)

def _assert_pmic_tune_register_run(result, report_file, summary):
    x = 0
    for i in result['expect']:
        if result['expect'][x][2] != result['return'][x][2]:
            if type(result['expect'][x][0]) == int:
                range = str(result['expect'][x][0])
            else:
                range = result['expect'][x][0]

                print( "Tune range run failed: Regulator "+result['regulator']+", Range: "+range+", Volt register value: "+str(hex(result['expect'][x][1]))+": Received: "+str(result['return'][x][2])+", Expected: "+str(result['expect'][x][2])+"\n", end='', file=report_file)
                print( "Tune range run failed: Regulator "+result['regulator']+", Range: "+range+", Volt register value: "+str(hex(result['expect'][x][1]))+": Received: "+str(result['return'][x][2])+", Expected: "+str(result['expect'][x][2])+"\n", end='', file=summary)
        x = x+1

    _assert_test(result, report_file, summary)

def _assert_pmic_voltage_run(result, report_file, summary):
    if result['product'] == 'bd9576' or result['product'] == 'bd96801':
        if result['expect'] != result['return']:
            print( "Voltage run failed (voltage check): Regulator "+result['regulator']+": Received: "+str(result['return'])+", Expected: "+str(result['expect'])+"\n", end='', file=report_file)
            print( "Voltage run failed (voltage check): Regulator "+result['regulator']+": Received: "+str(result['return'])+", Expected: "+str(result['expect'])+"\n", end='', file=summary)

    else:
        x = 0
        for i in result['expect']:
            if result['expect'][x][2] != result['return'][x][2]:
                    if type(result['expect'][x][0]) == int:
                        range = str(result['expect'][x][0])
                    else:
                        range = result['expect'][x][0]

                    print( "Voltage run failed: Regulator "+result['regulator']+", Range: "+range+", Volt register value: "+str(hex(result['expect'][x][1]))+": Received: "+str(result['return'][x][2])+", Expected: "+str(result['expect'][x][2])+"\n", end='', file=report_file)
                    print( "Voltage run failed: Regulator "+result['regulator']+", Range: "+range+", Volt register value: "+str(hex(result['expect'][x][1]))+": Received: "+str(result['return'][x][2])+", Expected: "+str(result['expect'][x][2])+"\n", end='', file=summary)
            x = x+1

    _assert_test(result, report_file, summary)

def _assert_pmic_regulator_is_on(result, report_file, summary):
    if result['expect'] != type(result['return']):
        print("Failed to check regulator enable state: Regulator '"+result['regulator']+"'. Return: "+str(result['return'])+", Should be "+str(result['expect'])+"\n", end='', file=report_file)
        print("Failed to check regulator enable state: Regulator '"+result['regulator']+"'. Return: "+str(result['return'])+", Should be "+str(result['expect'])+"\n", end='', file=summary)

    report_file.close()
    summary.close()
    assert result['expect'] == type(result['return'])

def _assert_pmic_regulator_is_on_driver(result, report_file, summary):
    if result['expect'] != result['return']:
        print("Regulator '"+result['regulator']+"' status mismatch! Return: "+str(result['return'])+", Should be "+str(result['expect'])+"\n", end='', file=report_file)
        print("Regulator '"+result['regulator']+"' status mismatch! Return: "+str(result['return'])+", Should be "+str(result['expect'])+"\n", end='', file=summary)

    _assert_test(result, report_file, summary)

def _assert_pmic_regulator_en(result, report_file, summary):
    if result['stage'] == 'regulator_enable':
        en_dis = 'enable'
    elif result['stage'] == 'regulator_disable':
        en_dis = 'disable'

    if result['expect'] != result['return']:
        print("Regulator '"+result['regulator']+"' "+en_dis+" failed!\n", end='', file=report_file)
        print("Regulator '"+result['regulator']+"' "+en_dis+" failed!\n", end='', file=summary)

    _assert_test(result, report_file, summary)

def _assert_pmic_disable_vr_fault(result, report_file, summary):
    if result['expect'] != result['return']:
        print( "Sanitycheck failed: Disable VR fault: "+result['stage']+": Expected: "+str(result['expect'])+". Received: "+str(result['return'])+".\n", end='', file=report_file)
        print( "Sanitycheck failed: Disable VR fault: "+result['stage']+": Expected: "+str(result['expect'])+". Received: "+str(result['return'])+".\n", end='', file=summary)
    _assert_test(result, report_file, summary)

def _assert_pmic_sanity_check_sysfs_set(result, report_file, summary):
    if result['expect'] != result['return']:
        print( "Sanitycheck failed: "+result['regulator']+": _set file missing in sysfs \n", end='', file=report_file)
        print( "Sanitycheck failed: "+result['regulator']+": _set file missing in sysfs \n", end='', file=summary)

    _assert_test(result, report_file, summary)

def _assert_pmic_sanity_check_sysfs_en(result, report_file, summary):
    if result['expect'] != result['return']:
        print( "Sanitycheck failed: "+result['regulator']+": _en file missing in sysfs \n", end='', file=report_file)
        print( "Sanitycheck failed: "+result['regulator']+": _en file missing in sysfs \n", end='', file=summary)
    _assert_test(result, report_file, summary)

def _assert_pmic_sanity_check(result, report_file, summary):
    if result['expect'] != result['return']:
        print( "Sanitycheck failed: "+result['regulator']+": device tree node missing for "+result['regulator']+"\n", end='', file=report_file)
        print( "Sanitycheck failed: "+result['regulator']+": device tree node missing for "+result['regulator']+"\n", end='', file=summary)
    _assert_test(result, report_file, summary)

def _assert_pmic_validate_config(result, report_file, summary):
    summary_written = 0
    #Basic info
    if result['product_name'] != result['expect_product_name']:
        print( "Sanitycheck failed: validate config: 'name' mismatch! Read: "+result['product_name']+". Expected: "+result['expect_product_name']+"\n", end='', file=report_file)
        print( "Sanitycheck failed: Validate config", end='', file=summary)
        summary_written = 1
    if result['i2c_bus_type'] != int:
        print( "Sanitycheck failed: validate config: i2c bus variable type is wrong! Expected int, got "+str(result['i2c_bus_type'])+"\n", end='', file=report_file)
        if summary_written == 0:
            print( "Sanitycheck failed: Validate config", end='', file=summary)
            summary_written = 1

    if result['i2c_address_type'] != int:
        print( "Sanitycheck failed: validate config: i2c address variable type is wrong! Expected int, got "+str(result['i2c_address_type'])+"\n", end='', file=report_file)
        if summary_written == 0:
            print( "Sanitycheck failed: Validate config", end='', file=summary)
            summary_written = 1

    #Regulator setting checks
    x = 0
    for i in result['expect']:
        if result['return'][x] != result['expect'][x]:

            if result['expect'][x][0] == 'volt_sel_bitmask':
                print( "Sanitycheck failed: validate config: Key '"+result['expect'][x][0]+"' at 'regulators > '"+str(result['expect'][x][1])+"' type is wrong! Expected "+str(result['expect'][x][2])+", got "+str(result['return'][x][2])+"\n", end='', file=report_file)
                if summary_written == 0:
                    print( "Sanitycheck failed: Validate config", end='', file=summary)
                    summary_written = 1

            if result['expect'][x][0] == 'step_mV':
                if type(result['expect'][x][2]) == int:
                    range = str(result['expect'][x][2])
                else:
                    range = result['expect'][x][2]
                print( "Sanitycheck failed: validate config: Key '"+result['expect'][x][0]+"' at 'regulators > "+str(result['expect'][x][1])+" > range > "+range+"' type is wrong! Expected "+str(result['expect'][x][3])+", got "+str(result['return'][x][3])+"\n", end='', file=report_file)
                if summary_written == 0:
                    print( "Sanitycheck failed: Validate config", end='', file=summary)
                    summary_written = 1

            if result['expect'][x][0] == 'list_mV':
                print( "Sanitycheck failed: validate config: Key '"+result['expect'][x][0]+"' at 'regulators > '"+str(result['expect'][x][1])+"' type is wrong! Expected number: "+str(result['expect'][x][2])+", got "+str(result['return'][x][2])+"\n", end='', file=report_file)
                if summary_written == 0:
                    print( "Sanitycheck failed: Validate config", end='', file=summary)
                    summary_written = 1

            if result['expect'][x][0] == 'sign_bitmask':
                print( "Sanitycheck failed: validate config: Key '"+result['expect'][x][0]+"' at 'regulators > '"+str(result['expect'][x][1])+"' type is wrong! Expected "+str(result['expect'][x][2])+", got "+str(result['return'][x][2])+"\n", end='', file=report_file)
                if summary_written == 0:
                    print( "Sanitycheck failed: Validate config", end='', file=summary)
                    summary_written = 1
        x = x+1

    report_file.close()
    summary.close()
    assert result['product_name'] == result['expect_product_name']
    assert result['i2c_bus_type'] == int
    assert result['i2c_address_type'] == int
    assert result['return'] == result['expect']

def check_result(result):
    report_file = open('../temp_results/temp_results.txt', 'a', encoding='utf-8')
    summary = open('../temp_results/summary.txt', 'a', encoding='utf-8')
    report_file.seek(0,2)
    summary.seek(0,2)

    if result['type'] == 'generic':
        if result['stage'] == 'ip_power':
            _assert_generic_ip_power(result, report_file, summary)
        elif result['stage'] == 'login':
            _assert_generic_login(result, report_file, summary)
        elif result['stage'] == 'init_overlay':
            _assert_generic_init_overlay(result, report_file, summary)
        elif result['stage'] == 'merge_dt_overlay' or result['stage'] == 'insmod_tests':
            _assert_generic_merge_dt_overlay_insmod_tests(result, report_file, summary)
        elif result['stage'] == 'get_dmesg':
            _assert_generic_get_dmesg(result, report_file, summary)
        elif result['stage'] == 'kunit_test':
            _assert_generic_kunit_test(result, report_file, summary)

    elif result['type'] == 'PMIC':
        #Sanity check:
        if result['stage'] == 'validate_config':
            _assert_pmic_validate_config(result, report_file, summary)
        elif result['stage'] == 'sanity_check':
            _assert_pmic_sanity_check(result, report_file, summary)
        elif result['stage'] == 'sanity_check_sysfs_set':
            _assert_pmic_sanity_check_sysfs_set(result, report_file, summary)
        elif result['stage'] == 'sanity_check_sysfs_en':
            _assert_pmic_sanity_check_sysfs_en(result, report_file, summary)
        elif result['stage'] == 'disable_vr_fault':
            _assert_pmic_disable_vr_fault(result, report_file, summary)

        #Regulator enable / disable:
        elif result['stage'] == 'regulator_enable' or result['stage'] == 'regulator_disable':
            _assert_pmic_regulator_en(result, report_file, summary)
        elif result['stage'] == 'regulator_is_on_driver':
            _assert_pmic_regulator_is_on_driver(result, report_file, summary)
        elif result['stage'] == 'regulator_is_on':
            _assert_pmic_regulator_is_on(result, report_file, summary)

        #Regulator voltages:
        elif result['stage'] == 'voltage_run' or result['stage'] == 'regulator_voltage_driver_get':
            _assert_pmic_voltage_run(result, report_file, summary)
        elif result['stage'] == 'tune_register_run':
            _assert_pmic_tune_register_run(result, report_file, summary)
        elif result['stage'] == 'out_of_range_voltages':
            _assert_pmic_out_of_range_voltages(result, report_file, summary)
        elif result['stage'] == 'read_dt_setting':
            _assert_pmic_read_dt_setting(result, report_file, summary)

    elif result['type'] == 'Sensor':
        if result['stage'] == 'test_gsel':
            _assert_sensor_test_gsel(result, report_file, summary)
        elif result['stage'] == 'gscale_raw_match':
            _assert_sensor_test_gscale_raw_match(result, report_file, summary)
        elif result['stage'] == 'test_sampling_frequency_match_timestamp':
            _assert_sensor_test_sampling_frequency_match_timestamp(result, report_file, summary)
