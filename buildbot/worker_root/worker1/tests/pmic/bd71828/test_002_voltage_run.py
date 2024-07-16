import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd71828
from test_util import check_result
from pmic_class import pmic
bd71828 = pmic(bd71828)

def test_voltage_run(command):
    for regulator in bd71828.board.data['regulators'].keys():
        if not 'dts_only' in bd71828.board.data['regulators'][regulator].keys():
            regulator_is_on=bd71828.regulator_is_on(regulator,command)
            if 'voltage' in bd71828.board.data['regulators'][regulator]['settings'].keys():
                if ("volt_change_not_allowed_while_on" in bd71828.board.data['regulators'][regulator] and regulator_is_on == 1):
                    print("Cannot change regulator: "+regulator+" voltage - Voltage run skipped.")
                elif 'range' not in bd71828.board.data['regulators'][regulator]['settings']['voltage'].keys():
                    print("Not a regulator")
                else:
                    result = bd71828.regulator_voltage_run(regulator,command)
                    check_result(result)
