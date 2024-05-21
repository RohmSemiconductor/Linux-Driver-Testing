import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd71837
from pmic_conf import pmic
bd71837 = pmic(bd71837)
print(sys.path)

def test_sanitycheck(command):
    bd71837.validate_config('bd71837')
    for regulator in bd71837.board.data['regulators'].keys():
        dt_buck_check = bd71837.sanity_check(regulator,command)
        assert dt_buck_check == 1

    for key in bd71837.board.data['debug']:
        vr_fault_status = bd71837.disable_vr_fault(key,command)
        assert vr_fault_status == bd71837.board.data['debug'][key]['setting']
