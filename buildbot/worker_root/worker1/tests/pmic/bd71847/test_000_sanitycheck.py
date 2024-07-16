import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd71847
from test_util import check_result
from pmic_class import pmic
bd71847 = pmic(bd71847)

def test_sanitycheck(command):
    result = bd71847.validate_config('bd71847')
    check_result(result)

    for regulator in bd71847.board.data['regulators'].keys():
        result = bd71847.sanity_check(regulator,command)
        check_result(result)

        result = bd71847.sanity_check_sysfs_en(regulator, command)
        check_result(result)

        result = bd71847.sanity_check_sysfs_set(regulator, command)
        check_result(result)

    for key in bd71847.board.data['debug']:
        result = bd71847.disable_vr_fault(key,command)
        check_result(result)
