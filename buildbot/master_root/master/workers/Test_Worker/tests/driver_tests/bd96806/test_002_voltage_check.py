import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd96806
from test_util import check_result
from pmic_class import pmic
bd96806 = pmic(bd96806)

def test_voltage_run(command):
    for regulator in bd96806.board.data['regulators'].keys():
        result = bd96806.regulator_voltage_driver_get(regulator,command)
        result['expect'] = bd96806.i2c_to_uv(regulator,command)
        print(result)
        check_result(result)
