import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd96806
from test_util import check_result
from pmic_class import pmic
bd96806 = pmic(bd96806)

def test_tune_register_run(command):
    for regulator in bd96806.board.data['regulators'].keys():
        if 'voltage_tune' in bd96806.board.data['regulators'][regulator]['settings'].keys():
            result=bd96806.regulator_tune_register_run(regulator, command)

            check_result(result)
