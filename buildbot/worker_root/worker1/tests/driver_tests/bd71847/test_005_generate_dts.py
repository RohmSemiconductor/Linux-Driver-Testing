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
conf_dts = 'ramprate2'
def test_dts():
    bd71847.generate_dts(conf_dts, 'configs/bd71847_gen_template.dts','configs/dts/bd71847/generated_dts_'+conf_dts+'.dts')
