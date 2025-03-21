import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd96801
from test_util import check_result
from pmic_class import pmic
bd96801 = pmic(bd96801)

def test_tune_register_run(command):
    for regulator in bd96801.board.data['regulators'].keys():
        if 'voltage_tune' in bd96801.board.data['regulators'][regulator]['settings'].keys():
            result=bd96801.regulator_tune_register_run(regulator, command)

            check_result(result)
