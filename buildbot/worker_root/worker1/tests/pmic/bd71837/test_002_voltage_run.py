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
        regulator_is_on=bd71837.regulator_is_on(regulator,command)
        if ("volt_change_not_allowed_while_on" in bd71837.board.data['regulators'][regulator] and regulator_is_on == 1):
            print("Cannot change regulator: "+regulator+" voltage - Voltage run skipped.")

        else:
            result = bd71837.regulator_voltage_run(regulator,command)
            check_result(result)
