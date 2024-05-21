import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd71837
from pmic_conf import pmic
bd71837 = pmic(bd71837)
print(sys.path)

def test_voltarge_run(command):
    test_failed =0
    failures=[]
    for regulator in bd71837.board.data['regulators'].keys():
        print(regulator)
        regulator_is_on=bd71837.regulator_is_on(regulator,command)
        if ("volt_change_not_allowed_while_on" in bd71837.board.data['regulators'][regulator] and regulator_is_on == 1):
            print("Cannot change regulator: "+regulator+" voltage - Voltage run skipped.")

        else:
            voltage_run=bd71837.regulator_voltage_run(regulator,command)
            if voltage_run['test_failed']==1:
                test_failed =1
                failures.append(voltage_run['buck_fail'])

    if test_failed == 1:
        bd71837.print_failures(failures)
    assert test_failed == 0
