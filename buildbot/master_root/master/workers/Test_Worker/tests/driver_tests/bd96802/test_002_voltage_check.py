import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd96802
from test_util import check_result
from pmic_class import pmic
bd96802 = pmic(bd96802)

def test_voltage_run(command):
    for regulator in bd96802.board.data['regulators'].keys():
        result = bd96802.regulator_voltage_driver_get(regulator,command)
        result['expect'] = bd96802.i2c_to_uv(regulator,command)
        print(result)
        check_result(result)
