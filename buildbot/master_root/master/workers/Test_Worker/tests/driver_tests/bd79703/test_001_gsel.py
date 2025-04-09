import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd79703
from test_util import check_result
from addac_class import addac
bd79703 = addac(bd79703)

def test_values(command):
    bd79703.get_sysfs_information(command)
    maxval = bd79703.bits_maxval()
#    for x in range(0, maxval+1):
    for x in range(0, 1):
        print(x)
#        stdout, stderr, returncode = bd79703._write_value(command, 1, x)
#        stdout, stderr, returncode = bd79703._read_value(command, 1, x)
#        print(stdout)
        result = bd79703.write_and_read_value(command, 1, x)
        joo, smooth_retval = bd79703._read_adc10x(command, 0)

    print("joo =")
    print(joo)
    print(smooth_retval)
#    print(result)
#    print("---CUT HERE---")
#    print(result['diff'])
    assert 1 == 0

#    check_result(result)
