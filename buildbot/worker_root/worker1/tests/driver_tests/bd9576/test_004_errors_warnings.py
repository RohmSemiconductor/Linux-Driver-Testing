import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd9576
from pmic_conf import pmic
bd9576 = pmic(bd9576)
print(sys.path)

def test_errors_warnings(command):
    for regulator in bd9576.board.data['regulators'].keys():
        print(regulator)
        for setting in bd9576.board.data['regulators'][regulator]['limit_settings'].keys():
            print(setting)
            dt_setting = bd9576.read_dt(regulator,'limit_settings', setting,command)
            print("Device tree value: "+str(dt_setting))
            i2c_read = bd9576.i2c_to_lim_uv(regulator, setting, command)
            print("Read from i2c: "+str(i2c_read))
            assert dt_setting == i2c_read
