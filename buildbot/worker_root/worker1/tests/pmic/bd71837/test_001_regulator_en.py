import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd71837
from test_util import check_result
from pmic_class import pmic
bd71837 = pmic(bd71837)

def test_regulator_en(command):
    for regulator in bd71837.board.data['regulators'].keys():
        if bd71837.check_regulator_enable_mode(regulator,command) == 1:
            result = bd71837.regulator_enable(regulator,command)
            check_result(result)
        
        if ((bd71837.check_regulator_enable_mode(regulator,command) == 1) and (bd71837.check_regulator_always_on_mode(regulator,command) == 0)):
            result = bd71837.regulator_disable(regulator,command)
            check_result(result)
