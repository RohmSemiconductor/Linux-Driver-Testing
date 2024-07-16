import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd71815
from test_util import check_result
from pmic_class import pmic
bd71815 = pmic(bd71815)

def test_voltage_run(command):
    for regulator in bd71815.board.data['regulators'].keys():
        if not 'dts_only' in bd71815.board.data['regulators'][regulator].keys():
            regulator_is_on=bd71815.regulator_is_on(regulator,command)

            if ("volt_change_not_allowed_while_on" in bd71815.board.data['regulators'][regulator] and regulator_is_on == 1):
                print("Cannot change regulator: "+regulator+" voltage - Voltage run skipped.")
            elif 'range' not in bd71815.board.data['regulators'][regulator]['settings']['voltage'].keys():
                print("Not a regulator")
            else:
                result = bd71815.regulator_voltage_run(regulator,command)
                check_result(result)
