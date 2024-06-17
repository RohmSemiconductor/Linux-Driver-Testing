import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd9576
from pmic_class import pmic
bd9576 = pmic(bd9576)
print(sys.path)

def test_out_of_range_voltages(command):
    test_failed =0
    failures=[]
    for regulator in bd9576.board.data['regulators'].keys():
        print(regulator)
        regulator_is_on=bd9576.regulator_is_on(regulator,command)

        if ("volt_change_not_allowed_while_on" in bd9576.board.data['regulators'][regulator] and regulator_is_on == 1):
            print("Cannot change regulator: "+regulator+" voltage - out of range tests skipped")

        elif 'volt_reg_bitmask' in bd9576.board.data['regulators'][regulator]:
            min, max = bd9576.get_min_max_volt(regulator)
            
            bd9576.regulator_voltage_driver_set(regulator,min,command)
            return_val_min = bd9576.i2c_to_uv(regulator,command)

            bd9576.regulator_voltage_driver_set(regulator,min-10000,command)
            return_val_try_less = bd9576.i2c_to_uv(regulator,command)
            
            assert return_val_min == return_val_try_less
            
            bd9576.regulator_voltage_driver_set(regulator,max,command)
            return_val_max = bd9576.i2c_to_uv(regulator,command)
            bd9576.regulator_voltage_driver_set(regulator,max+10000,command)
            return_val_try_more = bd9576.i2c_to_uv(regulator,command)
            
            assert return_val_max == return_val_try_more


#    test_fail = 0
#    assert test_fail == 1
