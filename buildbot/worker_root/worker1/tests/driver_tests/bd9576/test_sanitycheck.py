import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd9576
from pmic_conf import pmic
bd9576 = pmic(bd9576)
print(sys.path)

def test_sanitycheck(command):
    for regulator in bd9576.board.data['regulators'].keys():
        dt_buck_check = bd9576.sanity_check(regulator,command)
        assert dt_buck_check == 1
