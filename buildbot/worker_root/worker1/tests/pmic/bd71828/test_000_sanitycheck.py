import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd71828
from pmic_class import pmic
bd71828 = pmic(bd71828)
print(sys.path)

def test_sanitycheck(command):
    bd71828.validate_config('bd71828')
    for regulator in bd71828.board.data['regulators'].keys():
        dt_buck_check = bd71828.sanity_check(regulator,command)
        print(regulator)
        assert dt_buck_check == 1
        
        check_sysfs_en = bd71828.sanity_check_sysfs_en(regulator, command)
        assert check_sysfs_en == 1

        check_sysfs_set = bd71828.sanity_check_sysfs_set(regulator, command)
        assert check_sysfs_set == 1
