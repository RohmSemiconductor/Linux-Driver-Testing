import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd71847
from test_util import check_result
from pmic_class import pmic
bd71847 = pmic(bd71847)

def test_voltage_run(command):
    for regulator in bd71847.board.data['regulators'].keys():
        regulator_is_on=bd71847.regulator_is_on(regulator,command)
        check_result(regulator_is_on)

        if ("volt_change_not_allowed_while_on" in bd71847.board.data['regulators'][regulator] and regulator_is_on['return'] == 1):
            print("Cannot change regulator: "+regulator+" voltage - Voltage run skipped.")

        else:
            result = bd71847.regulator_voltage_run(regulator,command)
            check_result(result)
