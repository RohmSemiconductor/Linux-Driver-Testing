import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd71847
from test_util import check_result
from pmic_class import pmic
bd71847 = pmic(bd71847)

def test_004_ramprate1(command, dts):
    for regulator in bd71847.board.data['regulators'].keys():
        if 'settings' in bd71847.board.data['regulators'][regulator].keys():
            if 'ramprate' in bd71847.board.data['regulators'][regulator]['settings'].keys():
                result = bd71847.read_dt_setting(regulator, 'ramprate', dts,  command)
                result['return'] = [dts, 'ramprate', bd71847.i2c_to_ramprate_uv(regulator, command)]
                check_result(result)
