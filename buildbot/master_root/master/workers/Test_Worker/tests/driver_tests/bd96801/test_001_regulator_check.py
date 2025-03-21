import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd96801
from test_util import check_result
from pmic_class import pmic
bd96801 = pmic(bd96801)

def test_regulator_check(command):
    for regulator in bd96801.board.data['regulators'].keys():
        regulator_is_on = bd96801.regulator_is_on(regulator,command)
        check_result(regulator_is_on)

        if regulator_is_on['return'] == 1:
            result = bd96801.regulator_is_on_driver(regulator,command)
            result['expect'] = 1
            check_result(result)
