import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd71847_dts
from pmic_conf import pmic
bd71847 = pmic(bd71847_dts)
print(sys.path)

def test_004_default_dts(command):
    test_dts = 'default'
    property = 'ramprate'
    bd71847.test_dts_properties(command, test_dts, property)
#    for regulator in bd71847.board.dts['regulators'].keys():
#        if 'ramprate' in bd71847.board.dts['regulators'][regulator]['test'].keys():
#            i2c_return = i2c_read_dt_property('default', regulator,'ramprate')
#            assert i2c_return == bd71847.board.dts['regulators'][regulator]['test'][test_dts][property]['register_value']
