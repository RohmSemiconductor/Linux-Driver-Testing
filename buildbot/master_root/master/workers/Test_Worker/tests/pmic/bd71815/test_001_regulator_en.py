import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd71815
from test_util import check_result
from pmic_class import pmic
from time import sleep
bd71815 = pmic(bd71815)

def test_regulator_en(command):
    for regulator in bd71815.board.data['regulators'].keys():

        if not 'dts_only' in bd71815.board.data['regulators'][regulator].keys():

            if bd71815.check_regulator_enable_mode(regulator,command) == 1:
                result = bd71815.regulator_enable(regulator,command)
                check_result(result)

            if ((bd71815.check_regulator_enable_mode(regulator,command) == 1) and (bd71815.check_regulator_always_on_mode(regulator,command) == 0)):
                result = bd71815.regulator_disable(regulator,command)
                check_result(result)
    sleep(2)
