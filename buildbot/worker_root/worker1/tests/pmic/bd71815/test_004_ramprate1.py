import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd71815
from test_util import check_result
from pmic_class import pmic
bd71815 = pmic(bd71815)

def test_004_ramprate1(command, dts):
    for regulator in bd71815.board.data['regulators'].keys():
        if 'settings' in bd71815.board.data['regulators'][regulator].keys():
            if 'ramprate' in bd71815.board.data['regulators'][regulator]['settings'].keys():
                result = bd71815.read_dt_setting(regulator, 'ramprate', dts, command)
                result['return'] = [dts, 'ramprate', bd71815.i2c_to_ramprate_uv(regulator, command)]
                check_result(result)
