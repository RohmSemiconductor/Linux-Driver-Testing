import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd79701
from test_util import check_result
from addac_class import addac
bd79701 = addac(bd79701)

def test_sysfs_check(command):
    print(bd79701.board.data)
    result = bd79701.check_sysfs_information(command, addac='adc')
    check_result(result)

    result = bd79701.check_sysfs_information(command, addac='dac')
    check_result(result)
