import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd71815
from test_util import check_result
from pmic_class import pmic
bd71815 = pmic(bd71815)

def test_out_of_range_voltages(command):
    for regulator in bd71815.board.data['regulators'].keys():
        if not 'dts_only' in bd71815.board.data['regulators'][regulator].keys():
            if regulator != 'wled':
                regulator_is_on=bd71815.regulator_is_on(regulator,command)

                if ("volt_change_not_allowed_while_on" in bd71815.board.data['regulators'][regulator] and regulator_is_on == 1):
                    print("Cannot change regulator: "+regulator+" voltage - out of range tests skipped")

                else:
                    result, min, max = bd71815.get_min_max_volt(regulator)

                    bd71815.regulator_voltage_driver_set(regulator,min,command)
                    result['expect'] = ['min', bd71815.i2c_to_uv(regulator,command)]

                    bd71815.regulator_voltage_driver_set(regulator,min-10000,command)
                    result['return'] = ['min', bd71815.i2c_to_uv(regulator,command)]

                    check_result(result)

                    bd71815.regulator_voltage_driver_set(regulator,max,command)
                    result['expect'] = ['max', bd71815.i2c_to_uv(regulator,command)]

                    bd71815.regulator_voltage_driver_set(regulator,max+10000,command)
                    result['return'] = ['max', bd71815.i2c_to_uv(regulator,command)]

                    check_result(result)
