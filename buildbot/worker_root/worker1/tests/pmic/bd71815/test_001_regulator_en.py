import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd71815
from pmic_class import pmic
from time import sleep
bd71815 = pmic(bd71815)
print(sys.path)

def test_regulator_en(command):
    for regulator in bd71815.board.data['regulators'].keys():

        if not 'dts_only' in bd71815.board.data['regulators'][regulator].keys():

            if bd71815.check_regulator_enable_mode(regulator,command) == 1:
                regulator_en_status = bd71815.regulator_enable(regulator,command)
                assert regulator_en_status == bd71815.board.data['regulators'][regulator]['regulator_en_bitmask']

            regulator_en_status = bd71815.regulator_disable(regulator,command)

            if ((bd71815.check_regulator_enable_mode(regulator,command) == 1) and (bd71815.check_regulator_always_on_mode(regulator,command) == 0)):
                regulator_en_status = bd71815.regulator_disable(regulator,command)
                assert regulator_en_status == 0
    sleep(2)
