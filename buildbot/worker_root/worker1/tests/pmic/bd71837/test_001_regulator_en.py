import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd71837
from pmic_class import pmic
bd71837 = pmic(bd71837)
print(sys.path)

def test_regulator_en(command):
    for regulator in bd71837.board.data['regulators'].keys():
        if bd71837.check_regulator_enable_mode(regulator,command) == 1:
            regulator_en_status = bd71837.regulator_enable(regulator,command)
            assert regulator_en_status == bd71837.board.data['regulators'][regulator]['regulator_en_bitmask']
 
        regulator_en_status = bd71837.regulator_disable(regulator,command)
        
        if ((bd71837.check_regulator_enable_mode(regulator,command) == 1) and (bd71837.check_regulator_always_on_mode(regulator,command) == 0)):
            regulator_en_status = bd71837.regulator_disable(regulator,command)           
            assert regulator_en_status == 0
