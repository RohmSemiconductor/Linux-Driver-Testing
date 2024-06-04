import pytest
import sys
import os
import fileinput
from pathlib import Path
from datetime import date
sys.path.append(str(Path('./configs').absolute()))
import bd71847_dts
from pmic_conf import pmic
bd71847 = pmic(bd71847_dts)

today = date.today()
todaystr = today.strftime("%d-%m-%Y")
def test_dts():
    bd71847.generate_dts('protection_0','configs/bd71847_gen_template.dts','configs/dts/bd71847/generated_test_'+todaystr+'.dts')
    print(todaystr)
    test_fail = 0
    assert test_fail == 1
