import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd71828
from pmic_class import pmic
bd71828 = pmic(bd71828)
print(sys.path)

def test_004_ramprate1(command):
    for regulator in bd71828.board.data['regulators'].keys():
        print(regulator)
        if 'settings' in bd71828.board.data['regulators'][regulator].keys():
            if 'ramprate' in bd71828.board.data['regulators'][regulator]['settings'].keys():
                dt_setting = bd71828.read_dt_setting(regulator, 'ramprate', command)
                print(dt_setting)
                i2c_read = bd71828.i2c_to_ramprate_uv(regulator, command)
                assert i2c_read == dt_setting
