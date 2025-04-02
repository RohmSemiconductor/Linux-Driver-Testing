import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd96806
from test_util import check_result
from pmic_class import pmic
bd96806 = pmic(bd96806)

def test_004_ramprate1(command, dts):
    for regulator in bd96806.board.data['regulators'].keys():
        if 'settings' in bd96806.board.data['regulators'][regulator].keys():
            if 'ramprate' in bd96806.board.data['regulators'][regulator]['settings'].keys():
                result = bd96806.read_dt_setting(regulator, 'ramprate', dts,  command)
                result['return'] = [dts, 'ramprate', bd96806.i2c_to_ramprate_uv(regulator, command)]
                check_result(result)
