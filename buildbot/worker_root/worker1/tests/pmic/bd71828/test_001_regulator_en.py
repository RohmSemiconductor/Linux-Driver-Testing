import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd71828
from test_util import check_result
from pmic_class import pmic
bd71828 = pmic(bd71828)

def test_regulator_en(command):
    for regulator in bd71828.board.data['regulators'].keys():
        print(regulator)
        if not 'dts_only' in bd71828.board.data['regulators'][regulator].keys():

           # if 'idle_on' in bd71828.board.data['regulators'][regulator]['settings'].keys():
           #     idle_mode_status = bd71828.disable_idle_mode(regulator, command)
           #     assert idle_mode_status == 0

            if bd71828.check_regulator_enable_mode(regulator,command) == 1:
                result = bd71828.regulator_enable(regulator,command)
                check_result(result)

            if ((bd71828.check_regulator_enable_mode(regulator,command) == 1) and (bd71828.check_regulator_always_on_mode(regulator,command) == 0)):
                result = bd71828.regulator_disable(regulator,command)
                check_result(result)
