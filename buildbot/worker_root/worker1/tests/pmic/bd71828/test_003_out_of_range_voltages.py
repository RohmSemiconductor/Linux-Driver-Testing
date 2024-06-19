import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd71828
from pmic_class import pmic
bd71828 = pmic(bd71828)
print(sys.path)

def test_out_of_range_voltages(command):
    test_failed =0
    failures=[]
    for regulator in bd71828.board.data['regulators'].keys():
        if not 'dts_only' in bd71828.board.data['regulators'][regulator].keys():
            if regulator != 'wled': #CHANGE THIS!!!!!
                print(regulator)
                regulator_is_on=bd71828.regulator_is_on(regulator,command)

                if ("volt_change_not_allowed_while_on" in bd71828.board.data['regulators'][regulator] and regulator_is_on == 1):
                    print("Cannot change regulator: "+regulator+" voltage - out of range tests skipped")

                else:
                    min, max = bd71828.get_min_max_volt(regulator)

                    bd71828.regulator_voltage_driver_set(regulator,min,command)
                    return_val_min = bd71828.i2c_to_uv(regulator,command)

                    bd71828.regulator_voltage_driver_set(regulator,min-10000,command)
                    return_val_try_less = bd71828.i2c_to_uv(regulator,command)

                    assert return_val_min == return_val_try_less

                    bd71828.regulator_voltage_driver_set(regulator,max,command)
                    return_val_max = bd71828.i2c_to_uv(regulator,command)
                    bd71828.regulator_voltage_driver_set(regulator,max+10000,command)
                    return_val_try_more = bd71828.i2c_to_uv(regulator,command)

                    assert return_val_max == return_val_try_more
