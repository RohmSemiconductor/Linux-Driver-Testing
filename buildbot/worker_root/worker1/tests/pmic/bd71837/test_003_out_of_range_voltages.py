import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd71837
from test_util import check_result
from pmic_class import pmic
bd71837 = pmic(bd71837)

def test_out_of_range_voltages(command):
    for regulator in bd71837.board.data['regulators'].keys():
        regulator_is_on=bd71837.regulator_is_on(regulator,command)
        check_result(regulator_is_on)

        if ("volt_change_not_allowed_while_on" in bd71837.board.data['regulators'][regulator] and regulator_is_on['return'] == 1):
            print("Cannot change regulator: "+regulator+" voltage - out of range tests skipped")

        else:
            result, min, max = bd71837.get_min_max_volt(regulator)

            bd71837.regulator_voltage_driver_set(regulator,min,command)
            result['expect'] = ['min', bd71837.i2c_to_uv(regulator,command)]

            bd71837.regulator_voltage_driver_set(regulator,min-10000,command)
            result['return'] = ['min', bd71837.i2c_to_uv(regulator,command)]

            check_result(result)

            bd71837.regulator_voltage_driver_set(regulator,max,command)
            result['expect'] = ['max', bd71837.i2c_to_uv(regulator,command)]
            bd71837.regulator_voltage_driver_set(regulator,max+10000,command)
            result['return'] = ['max', bd71837.i2c_to_uv(regulator,command)]

            check_result(result)
