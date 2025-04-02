import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd96805
from test_util import check_result
from pmic_class import pmic
bd96805 = pmic(bd96805)

def test_voltage_run(command):
    for regulator in bd96805.board.data['regulators'].keys():
        result = bd96805.regulator_voltage_driver_get(regulator,command)
        result['expect'] = bd96805.i2c_to_uv(regulator,command)
        print(result)
        check_result(result)
