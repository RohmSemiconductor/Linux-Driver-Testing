import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd71847
from pmic_conf import pmic
bd71847 = pmic(bd71847)
print(sys.path)

def test_004_ramprate1(command):
    for regulator in bd71847.board.data['regulators'].keys():
        print(regulator)
        if 'settings' in bd71847.board.data['regulators'][regulator].keys():
            if 'ramprate' in bd71847.board.data['regulators'][regulator]['settings'].keys():
                dt_setting = bd71847.read_dt_setting(regulator, 'ramprate', command)
                print(dt_setting)
                i2c_read = bd71847.i2c_to_ramprate_uv(regulator, command)
                assert i2c_read == dt_setting
