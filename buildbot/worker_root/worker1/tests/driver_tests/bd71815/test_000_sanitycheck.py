import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd71815
from pmic_conf import pmic
bd71815 = pmic(bd71815)
print(sys.path)

def test_sanitycheck(command):
    bd71815.validate_config('bd71815')
    for regulator in bd71815.board.data['regulators'].keys():
        if 'range' not in bd71815.board.data['regulators'][regulator].keys():
            dt_buck_check = bd71815.sanity_check(regulator,command)
            print(regulator)
            assert dt_buck_check == 1
