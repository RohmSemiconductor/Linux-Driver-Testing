import sys
import pytest
import difflib
import copy
sys.path.append('..')
from test_util import check_result, result

def test_get_kunit(command,kunit_test, product):
    result['type'] = 'generic'
    result['stage'] = 'get_kunit'
    result['expect'] = 0

    stdout, stderr, returncode = command.run('dmesg')
    dmesg = copy.copy(stdout)

    if kunit_test == 'test_linear_ranges':
        stdout, stderr, returncode = command.run('modprobe test_linear_ranges')
        kunit_returncode = copy.copy(returncode)
    if kunit_test == 'iio_test_gts':
        stdout, stderr, returncode = command.run('modprobe iio-test-gts')
        kunit_returncode = copy.copy(returncode)

    stdout, stderr, returncode = command.run('dmesg')
    kunit_dmesg = copy.copy(stdout)

    kunit_file = open('../temp_results/'+product+'/kunit_'+kunit_test+'_output.txt', 'w+', encoding='utf-8')

    x =0
    y= 0

    for line in dmesg:
        x=x+1
    for line2 in kunit_dmesg:
        if y>= x:
            print(kunit_dmesg[y]+'\n', end='', file=kunit_file)
        y=y+1

    kunit_file.close()
    result['return'] = kunit_returncode
    check_result(result)
