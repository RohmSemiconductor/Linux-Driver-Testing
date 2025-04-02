import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd96802
from test_util import check_result
from pmic_class import pmic
bd96802 = pmic(bd96802)

def test_tune_register_run(command):
    for regulator in bd96802.board.data['regulators'].keys():
        if 'voltage_tune' in bd96802.board.data['regulators'][regulator]['settings'].keys():
            result=bd96802.regulator_tune_register_run(regulator, command)

            check_result(result)
