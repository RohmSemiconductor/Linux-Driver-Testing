import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd71815
from pmic_class import pmic
bd71815 = pmic(bd71815)
print(sys.path)

def test_voltage_run(command):
    test_failed =0
    failures=[]
    for regulator in bd71815.board.data['regulators'].keys():
        print(regulator)
        if not 'dts_only' in bd71815.board.data['regulators'][regulator].keys():
            regulator_is_on=bd71815.regulator_is_on(regulator,command)

            if ("volt_change_not_allowed_while_on" in bd71815.board.data['regulators'][regulator] and regulator_is_on == 1):
                print("Cannot change regulator: "+regulator+" voltage - Voltage run skipped.")
            elif 'range' not in bd71815.board.data['regulators'][regulator]['settings']['voltage'].keys():
                print("Not a regulator")
            else:
                voltage_run=bd71815.regulator_voltage_run(regulator,command)
                if voltage_run['test_failed']==1:
                    test_failed = 1
                    failures.append(voltage_run['buck_fail'])

    if test_failed == 1:
        bd71815.print_failures(failures)
    assert test_failed ==0
