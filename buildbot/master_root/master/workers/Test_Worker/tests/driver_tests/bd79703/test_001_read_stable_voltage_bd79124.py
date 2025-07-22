import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd79124
from test_util import check_result
from addac_class import addac
bd79124 = addac(bd79124)

def test_read_stable_voltage(command):
    result = bd79124.check_stable_voltage(command, bd79124.board.data['info']['stable_voltage_channel'], 150)

    check_result(result)
