import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd96805
from test_util import check_result
from pmic_class import pmic
bd96805 = pmic(bd96805)

def test_tune_register_run(command):
    for regulator in bd96805.board.data['regulators'].keys():
        if 'voltage_tune' in bd96805.board.data['regulators'][regulator]['settings'].keys():
            result=bd96805.regulator_tune_register_run(regulator, command)

            check_result(result)
