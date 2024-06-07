import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd71847_dts
from pmic_conf import pmic
bd71847 = pmic(bd71847_dts)
print(sys.path)

def test_001_ramprate2_dts(command):
    test_dts = 'ramprate2'
    property = 'ramprate'
    bd71847.test_dts_properties(command, test_dts, property)
