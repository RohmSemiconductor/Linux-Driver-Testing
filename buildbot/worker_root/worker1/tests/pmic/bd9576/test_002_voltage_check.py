import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd9576
from pmic_class import pmic
bd9576 = pmic(bd9576)
print(sys.path)

def test_voltage_run(command):
    for regulator in bd9576.board.data['regulators'].keys():
        if regulator == 'VOUTS1':
            assert bd9576.regulator_voltage_driver_get(regulator,command) == bd9576.mv_to_uv(3300) 
        else:
            assert bd9576.regulator_voltage_driver_get(regulator,command) == bd9576.i2c_to_uv(regulator,command)
