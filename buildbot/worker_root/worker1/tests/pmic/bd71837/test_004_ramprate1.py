import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd71837
from pmic_class import pmic
bd71837 = pmic(bd71837)
print(sys.path)

def test_004_ramprate1(command):
    for regulator in bd71837.board.data['regulators'].keys():
        print(regulator)
        if 'settings' in bd71837.board.data['regulators'][regulator].keys():
            if 'ramprate' in bd71837.board.data['regulators'][regulator]['settings'].keys():
                dt_setting = bd71837.read_dt_setting(regulator, 'ramprate', command)
                print(dt_setting)
                i2c_read = bd71837.i2c_to_ramprate_uv(regulator, command)
                print(i2c_read)
                assert i2c_read == dt_setting
