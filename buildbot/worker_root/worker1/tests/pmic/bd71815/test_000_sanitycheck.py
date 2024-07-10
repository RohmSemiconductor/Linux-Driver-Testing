import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd71815
from pmic_class import pmic
bd71815 = pmic(bd71815)
print(sys.path)

def test_sanitycheck(command):
    bd71815.validate_config('bd71815')
    for regulator in bd71815.board.data['regulators'].keys():
        dt_buck_check = bd71815.sanity_check(regulator,command)
        print(regulator)
        assert dt_buck_check == 1
        if 'dts_only' not in bd71815.board.data['regulators'][regulator].keys(): 
            check_sysfs_en = bd71815.sanity_check_sysfs_en(regulator, command)
            assert check_sysfs_en == 1

            check_sysfs_set = bd71815.sanity_check_sysfs_set(regulator, command)
            assert check_sysfs_set == 1
