import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd96801
from test_util import check_result
from pmic_class import pmic
bd96801 = pmic(bd96801)

def test_voltage_run(command):
    for regulator in bd96801.board.data['regulators'].keys():
        result = bd96801.regulator_voltage_driver_get(regulator,command)
        result['expect'] = bd96801.i2c_to_uv(regulator,command)
        print(result)
        check_result(result)
