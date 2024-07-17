import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd9576
from test_util import check_result
from pmic_class import pmic
bd9576 = pmic(bd9576)

def test_ovd_uvd(command, dts):
    for regulator in bd9576.board.data['regulators'].keys():
        for setting in bd9576.board.data['regulators'][regulator]['settings'].keys():
            if setting != 'voltage':
                result = bd9576.read_dt_setting(regulator, setting, dts, command)
                result['return'] = [dts, setting, bd9576.i2c_to_lim_uv(regulator, setting, command)]
                check_result(result)
