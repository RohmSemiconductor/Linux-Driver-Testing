import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd96802
from test_util import check_result
from pmic_class import pmic
bd96802 = pmic(bd96802)

def test_004_ramprate1(command, dts):
    for regulator in bd96802.board.data['regulators'].keys():
        if 'settings' in bd96802.board.data['regulators'][regulator].keys():
            if 'ramprate' in bd96802.board.data['regulators'][regulator]['settings'].keys():
                result = bd96802.read_dt_setting(regulator, 'ramprate', dts,  command)
                result['return'] = [dts, 'ramprate', bd96802.i2c_to_ramprate_uv(regulator, command)]
                check_result(result)
