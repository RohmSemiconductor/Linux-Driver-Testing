import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd71847
from pmic_conf import pmic
bd71847 = pmic(bd71847)
print(sys.path)

def test_regulator_en(command):
    for regulator in bd71847.board.data['regulators'].keys():
        if bd71847.check_regulator_enable_mode(regulator,command) == 1:
            regulator_en_status = bd71847.regulator_enable(regulator,command)
            assert regulator_en_status == bd71847.board.data['regulators'][regulator]['regulator_en_bitmask']
 
        regulator_en_status = bd71847.regulator_disable(regulator,command)
        
        if ((bd71847.check_regulator_enable_mode(regulator,command) == 1) and (bd71847.check_regulator_always_on_mode(regulator,command) == 0)):
            regulator_en_status = bd71847.regulator_disable(regulator,command)           
            assert regulator_en_status == 0
