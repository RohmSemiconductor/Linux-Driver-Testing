import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd71847
from pmic_conf import pmic
bd71847 = pmic(bd71847)
print(sys.path)

def test_out_of_range_voltages(command):
    test_failed =0
    failures=[]
    for regulator in bd71847.board.data['regulators'].keys():
        print(regulator)
        regulator_is_on=bd71847.regulator_is_on(regulator,command)

        if ("volt_change_not_allowed_while_on" in bd71847.board.data['regulators'][regulator] and regulator_is_on == 1):
            print("Cannot change regulator: "+regulator+" voltage - out of range tests skipped")

        else:
            min, max = bd71847.get_min_max_volt(regulator)
            
            bd71847.regulator_voltage_driver_set(regulator,min,command)
            return_val_min = bd71847.regulator_voltage_get(regulator,command)

            bd71847.regulator_voltage_driver_set(regulator,min-10000,command)
            return_val_try_less = bd71847.regulator_voltage_get(regulator,command)
            
            assert return_val_min == return_val_try_less
            
            bd71847.regulator_voltage_driver_set(regulator,max,command)
            return_val_max = bd71847.regulator_voltage_get(regulator,command)
            bd71847.regulator_voltage_driver_set(regulator,max+10000,command)
            return_val_try_more = bd71847.regulator_voltage_get(regulator,command)
            
            assert return_val_max == return_val_try_more


#    test_fail = 0
#    assert test_fail == 1
