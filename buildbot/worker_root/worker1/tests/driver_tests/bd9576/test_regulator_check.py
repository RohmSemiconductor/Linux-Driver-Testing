import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd9576
from pmic_conf import pmic
bd9576 = pmic(bd9576)
print(sys.path)

def test_regulator_check(command):
    vout1_en_low=bd9576.check_bd9576_vout1_en_low(command)

    for regulator in bd9576.board.data['regulators'].keys():
        regulator_is_on = bd9576.regulator_is_on(regulator,command)
        if regulator == 'buck1' and vout1_en_low == 1:
            assert bd9576.regulator_is_on_driver(regulator,command) == 0
        elif regulator_is_on == 1:
            assert bd9576.regulator_is_on_driver(regulator,command) == 1
