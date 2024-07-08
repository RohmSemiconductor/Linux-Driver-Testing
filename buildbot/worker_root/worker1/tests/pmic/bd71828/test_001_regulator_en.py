import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd71828
from pmic_class import pmic
bd71828 = pmic(bd71828)
print(sys.path)

def test_regulator_en(command):
    for regulator in bd71828.board.data['regulators'].keys():
        print(regulator)
        if not 'dts_only' in bd71828.board.data['regulators'][regulator].keys():

           # if 'idle_on' in bd71828.board.data['regulators'][regulator]['settings'].keys():
           #     idle_mode_status = bd71828.disable_idle_mode(regulator, command)
           #     assert idle_mode_status == 0

            if bd71828.check_regulator_enable_mode(regulator,command) == 1:
                regulator_en_status = bd71828.regulator_enable(regulator,command)
                assert regulator_en_status == bd71828.board.data['regulators'][regulator]['regulator_en_bitmask']

            if ((bd71828.check_regulator_enable_mode(regulator,command) == 1) and (bd71828.check_regulator_always_on_mode(regulator,command) == 0)):
                regulator_en_status = bd71828.regulator_disable(regulator,command)
                assert regulator_en_status == 0
