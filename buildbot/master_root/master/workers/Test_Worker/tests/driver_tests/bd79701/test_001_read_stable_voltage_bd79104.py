import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd79104
from test_util import check_result
from addac_class import addac
bd79104 = addac(bd79104)

def test_read_stable_voltage(command):
    result = bd79104.check_stable_voltage(command, bd79104.board.data['info']['stable_voltage_channel'], 50)
    print(result)

    check_result(result)
