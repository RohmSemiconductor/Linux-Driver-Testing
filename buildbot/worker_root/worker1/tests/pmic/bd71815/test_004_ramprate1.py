import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd71815
from pmic_class import pmic
bd71815 = pmic(bd71815)
print(sys.path)

def test_004_ramprate1(command):
    for regulator in bd71815.board.data['regulators'].keys():
        print(regulator)
        if 'settings' in bd71815.board.data['regulators'][regulator].keys():
            if 'ramprate' in bd71815.board.data['regulators'][regulator]['settings'].keys():
                dt_setting = bd71815.read_dt_setting(regulator, 'ramprate', command)
                print(dt_setting)
                i2c_read = bd71815.i2c_to_ramprate_uv(regulator, command)
                assert i2c_read == dt_setting
