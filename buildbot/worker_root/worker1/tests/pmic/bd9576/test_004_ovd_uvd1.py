import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd9576
from pmic_class import pmic
bd9576 = pmic(bd9576)
print(sys.path)

def test_ovd_uvd(command):
    for regulator in bd9576.board.data['regulators'].keys():
        print(regulator)
        for setting in bd9576.board.data['regulators'][regulator]['settings'].keys():
            if setting != 'voltage':
                print('ovd')
                dt_setting = bd9576.read_dt_setting(regulator, setting, command)
                print("Device tree value: "+str(dt_setting))
                i2c_read = bd9576.i2c_to_lim_uv(regulator, setting, command)
                print("Read from i2c: "+str(i2c_read))
                assert dt_setting == i2c_read
