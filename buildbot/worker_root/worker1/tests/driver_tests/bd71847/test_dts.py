import pytest
import sys
import os
import fileinput
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd71847_dts
from pmic_conf import pmic
bd71847 = pmic(bd71847_dts)
print(sys.path)



def test_dts():
    bd71847.generate_dts('protection_0','configs/bd71847_gen_template.dts','new_dts.dts')
    test_fail = 0
    assert test_fail == 1
