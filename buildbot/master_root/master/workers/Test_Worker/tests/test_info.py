
### PMIC:
test_info = {}
test_info['header']="---------------------------------- TEST INFO ----------------------------------"
test_info['footer']="-------------------------------------------------------------------------------\n"

### GENERIC TESTS
test_info['generic']={
'check_iio_generic_buffer':test_info['header']+
"""
This stage checks that the iio_generic_buffer binary is in the NFS.
"""
+test_info['footer']
,

'login':test_info['header']+
"""
This stage:
1. switches power first off, then on
2. waits 75 seconds for the login prompt before returning to step 1. up to 5 times
3. Logs in with beagle#.yaml login information
4. Runs 'cat /proc/version' on BeagleBone Black and checks that 'Linux' can be found
5. Runs 'false' on BeagleBone Black and checks that returncode is different than 0
"""
+test_info['footer']
,

'init_overlay':test_info['header']+
"""
This step installs mva_overlay.ko and checks that success with 'lsmod'.
"""
+test_info['footer']
,

'merge_dt_overlay':test_info['header']+
"""
This step installs devicetree overlays listed in the kernel_modules.py

Assert success by checking that the modules listed in the kernel_modules.py can
be found in the output of 'lsmod'.
"""
+test_info['footer']
,

'insmod_tests':test_info['header']+
"""
This step installs test kernel modules with 'insmod' command.

Success is asserted by reading the output of 'lsmod' that the correct modules
are loaded. List of modules to check is listed in the kernel_modules.py.
"""
+test_info['footer']
,

'insmod_accel_tests':test_info['header']+
"""
This step installs accelerometer test module.

1. Find out kernel version with 'uname -r'
2. Copy kernel modules listed in the kernel_modules.py from the root of NFS
   to /lib/modules/<kernel_version>/kernel/
3. Run 'depmod'
4. Run 'modprobe <module_name> with module names found from the kernel_modules.py,
   stripping the file extension.
5. Assert success by parsing the output of 'lsmod' and check that the modules
   listed in kernel_modules.py can be found.
"""
+test_info['footer']
,

'get_dmesg':test_info['header']+
"""
This step runs 'dmesg' on the target BeagleBone Black.
Expected result is returncode 0.
"""
+test_info['footer']
,
'kunit_test':test_info['header']+
"""
This test parses the kunit out of dmesg.

Kunit test success is determined by checking the kunit_dmesg part for "not ok".
"""
+test_info['footer']
,
}
### /GENERIC TESTS

### PMIC TESTS
test_info['pmic']={
'sanitycheck':test_info['header']+
"""
This test checks:
- configs/BDxxxxx.py file structure is about correct
- sysfs files named in the config can be found
- regulators can be found from /proc/device-tree path
- Additionally vr_fault register settings are changed here if needed for the PMIC
"""
+test_info['footer']
,

'regulator_en':test_info['header']+
"""
This test enables and disables regulators if the PMIC allows them, and asserts
success from reading the components register via I2C.
"""
+test_info['footer']
,

'voltage_run':test_info['header']+
"""
This test sets all allowed values for regulators whose voltage can be changed.
Settings are written using the sysfs interface provided by a test kernel module.
Success is asserted from reading the components register via I2C.
"""
+test_info['footer']
,
'tune_register_run':test_info['header']+
"""
This test checks that using the tune register works by using the sysfs interface
provided by a test kernel module.

Current voltage is first read from the i2c register before trying to write 'tuned'
values via sysfs interface.

Written value is compared to read sum of voltage register + tune register converted
to microvolt.
"""
+test_info['footer']
,

'regulator_voltage_driver_get':test_info['header']+
"""
This test reads the voltage from driver, using the sysfs interface provided
by a test kernel module. Read value is compared to what is read from the
component register.
"""
+test_info['footer']
,

'out_of_range_voltages':test_info['header']+
"""
This tests:
- Finds the minimum and maximum voltages for each regulator
- Sets the voltage to min/max
- Tries to set the voltage below min / over max
- Asserts that nothing happened in the voltage register
"""
+test_info['footer']
,

'read_dt_setting':test_info['header']+
"""
This test read devicetree value from /proc/device-tree,
and compares that to what is written to components register.
"""
+test_info['footer']
,

'regulator_is_on':test_info['header']+
"""
regulator_is_on():
This stage is precursor to checking that regulator enable state which can't be
changed can be read.

This is used for voltage run tests as well to first check if its normal that
regulators voltage setting can not be changed.

In the case of PMIC tested being BD71837 / BD71847:
/proc/device-tree/.../rohm,no-regulator-enable-control is checked if it exists
to determine whether enable mode can be changed.
"""
+test_info['footer']
,

'regulator_is_on_driver':test_info['header']+
"""
Regulator check test use regulator_is_on_driver() together with
regulator_is_on() to assert that the enable state read from sysfs interface
provided by a test kernel module matches the expected value.
"""
+test_info['footer']
,

'voltage_check':test_info['header']+
"""
This tests checks that regulator VOUTS1 voltage is 3.3V, for other regulator
the voltage reported from sysfs _set file is compared to one read from the
voltage register via I2C.
"""
+test_info['footer']
,

'ramprate':test_info['header']+
"""
Ramprate test reads the setting from /proc/device-tree and compares that value
to one read from the component register via i2c.
"""
+test_info['footer']
,

'ovd_uvd_read':
"""
OVD_UVD test reads device tree settings from the /proc/device-tree.
Read settings are:
regulator-ov-error-microvolt
regulator-uv-error-microvolt
regulator-ov-warn-microvolt
regulator-uv-warn-microvolt
regulator-oc-warn-microamp
regulator-oc-protection-microamp
"""
+test_info['footer']
,

'ovd_uvd_disable':test_info['header']+
"""
This test disables protection, warning and error settings with these devicetree properties:
regulator-ov-error-microvolt
regulator-uv-error-microvolt
regulator-ov-warn-microvolt
regulator-uv-warn-microvolt
regulator-oc-warn-microamp
regulator-oc-protection-microamp

And reads the component's register via I2C to assert that disabling was succesful"
"""
+test_info['footer']
,
}

### /PMIC TESTS
    ### PMIC RTC TESTS
test_info['rtc'] = {
'reset_and_check_date':test_info['header']+
"""
RTC test:
This test is done using 'hwclock' command with a /dev/rtc_file

Set component time to what is found in config file rtc -> rtc_reset
Get component datime and split it to date and time parts

Compare Set date to Get date
"""
+test_info['footer']
,

'set_rtc_from_srv_time':test_info['header']+
"""
RTC test:
This test is done using 'hwclock' command with a /dev/rtc_file

This stage sets the given RTC to test server systemtime.

Test server systemtime and RTC time is fetched in "since epoch" format and compared.
"""
+test_info['footer']
,

'set_bbb_from_rtc_time':test_info['header']+
"""
RTC test:
This test is done using 'hwclock' command with a /dev/rtc_file

This stage sets BBB systemtime from the given RTC time.

BBB systemtime and RTC time is fetched in "since epoch" format and compared.
"""
+test_info['footer']
,

'set_rtc_from_bbb_sys_time':test_info['header']+
"""
RTC test:
This test is done using 'hwclock' command with a /dev/rtc_file

This stage sets the given RTC to BBB systemtime.

RTC time and BB systemtime is fetched in "since epoch" format and compared.
"""
+test_info['footer']
,
    ## /PMIC RTC TESTS
}
### ACCELEROMETER TESTS
test_info['accelerometer'] = {
'gsel':test_info['header']+
"""
This test writes G-scale value to a sysfs file provided by the IIO subsystem
and compares that value to the gsel value fetched from configuration file.

The value is fetched from a list by using the value read component register as
the lists index number.
"""
+test_info['footer']
,

'gscale_raw_match':test_info['header']+ ###KATOPPA NYT TÄMÄ VIELÄ
"""
This test goes through all the G-scale values.
This test uses only 1 channel at a time.
"""
+test_info['footer']
,
'sampling_frequency':test_info['header']+
"""
This test reads timestamps from multiple samples using the iio sysfs interface.
Function to exact number of samples is: roundup(freqHz)*2*5

The interval is counted between each sample, sampling frequency Hz converted to
nanoseconds is substracted from that. Perfect result would be 0, but slight
tolerance is added to both directions when comparing results.
"""
+test_info['footer']
,

'gscale_ms2':test_info['header']+
"""
This reads the m/s² value from the iio sysfs interface and compares that value
to a m/s² value that is calculated from the hardware register with a bit of tolerance.
"""
+test_info['footer']

}
### /ACCELEROMETER TESTS

### ADDAC TESTS
test_info['addac'] = {
'check_sysfs_information':test_info['header']+
"""
This is a sanity check type of test, that checks that the iio sysfs device files
can be found. The test script tests tries to find ADC files first, then DAC files.
"""
+test_info['footer']
,

'read_stable_voltage':test_info['header']+
"""
This test reads a ADC channel which has 1.8v input from BeagleBoneBlack analog
voltage block. The read result is compared to the expected 1800mV with a bit
of tolerance.

To read the ADC channel, iio sysfs interface is used.
"""
+test_info['footer']
,

'write_read':test_info['header']+
"""
This test reads through every value in every channel from a tested DAC.

1. Use iio sysfs interface to write the value for a channel
2. Get information to which ADC channel the DAC channel is connected to.
   Information is stored in the DACs config file.
3. Use read_adc10x.sh (located in the NFS) to read multiple ADC alues to
   reduce noise.
4. Calculate mean value from the read samples
5. Calculate volt value from the mean value
6. Calculate DAC output voltage from the value looped in the test and the
   multiplier found from the iio sysfs file.
7. Compare results with a bit of tolerance.
8. If a channel passes the test, reset DAC output voltage to 0V.
"""
+test_info['footer']
}
