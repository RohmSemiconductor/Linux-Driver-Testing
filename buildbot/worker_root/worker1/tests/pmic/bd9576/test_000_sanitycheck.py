import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd9576
from pmic_class import pmic
bd9576 = pmic(bd9576)
print(sys.path)

def test_sanitycheck(command):
    bd9576.validate_config('bd9576')
    for regulator in bd9576.board.data['regulators'].keys():
        dt_buck_check = bd9576.sanity_check(regulator,command)
        assert dt_buck_check == 1

        check_sysfs_en = bd9576.sanity_check_sysfs_en(regulator, command)
        assert check_sysfs_en == 1
        check_sysfs_set = bd9576.sanity_check_sysfs_set(regulator, command)
        assert check_sysfs_set == 1
