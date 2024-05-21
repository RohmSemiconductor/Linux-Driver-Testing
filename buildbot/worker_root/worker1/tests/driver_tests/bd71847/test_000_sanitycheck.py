import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd71847
from pmic_conf import pmic
bd71847 = pmic(bd71847)
print(sys.path)

def test_sanitycheck(command):
    bd71847.validate_config('bd71847')
    for regulator in bd71847.board.data['regulators'].keys():
        dt_buck_check = bd71847.sanity_check(regulator,command)
        assert dt_buck_check == 1

    for key in bd71847.board.data['debug']:
        vr_fault_status = bd71847.disable_vr_fault(key,command)
        assert vr_fault_status == bd71847.board.data['debug'][key]['setting']
