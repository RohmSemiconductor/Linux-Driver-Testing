import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd71837
from test_util import check_result
from pmic_class import pmic
bd71837 = pmic(bd71837)

def test_voltarge_run(command):
    for regulator in bd71837.board.data['regulators'].keys():
        result=bd71837.regulator_is_on(regulator,command)
        check_result(result)
        if ("volt_change_not_allowed_while_on" in bd71837.board.data['regulators'][regulator] and result['return'] == 1):
            print("Cannot change regulator: "+regulator+" voltage - Voltage run skipped.")

        else:
            result = bd71837.regulator_voltage_run(regulator,command)
            check_result(result)
