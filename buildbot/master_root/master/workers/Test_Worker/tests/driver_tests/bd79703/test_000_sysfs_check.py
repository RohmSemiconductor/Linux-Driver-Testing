import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd79703
from test_util import check_result
from addac_class import addac
bd79703 = addac(bd79703)

def test_sysfs_check(command):
    result = bd79703.check_sysfs_information(command, addac='adc')
    check_result(result)

    result = bd79703.check_sysfs_information(command, addac='dac')
    check_result(result)
