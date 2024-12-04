import sys
import pytest
import difflib
import copy
sys.path.append('..')
from test_util import check_result, result, checkStdOut

def test_get_kunit(command,kunit_test):
    result['type'] = 'generic'
    result['stage'] = 'kunit_test'
    result['substage'] = kunit_test
    result['expect'] = None
    result['result_dir'] = 'linux'

    ### Get kernel log before installing Kunit modules
    ### This needs to be done so that we can only get the results that we want
    stdout, stderr, returncode = command.run('dmesg')
    dmesg_before_kunit = copy.copy(stdout)

    ###  Dedice which Kunit test module to install
    if kunit_test == 'test_linear_ranges':
        stdout, stderr, returncode = command.run('modprobe test_linear_ranges')

    if kunit_test == 'iio_test_gts':
        stdout, stderr, returncode = command.run('modprobe iio-test-gts')

    ### Get kernel log after installing the Kunit test.
    ### At this point the kernel log has the Kunit test output
    stdout, stderr, returncode = command.run('dmesg')
    dmesg_after_kunit = copy.copy(stdout)
    result['kunit_full_dmesg'] = dmesg_after_kunit
    x = 0
    y = 0

    result['kunit_dmesg'] = []

    for line in dmesg_before_kunit:
        x = x+1
    for line2 in dmesg_after_kunit:
        if y >= x:
            result['kunit_dmesg'].append(dmesg_after_kunit[y])
        y = y+1

    ### result['return'] == 0 if Kunit test fails
    result['return'] = checkStdOut(result['kunit_dmesg'], "not ok")

    check_result(result)
