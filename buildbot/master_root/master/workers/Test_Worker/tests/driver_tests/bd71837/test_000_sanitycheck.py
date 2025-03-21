import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd71837
from test_util import check_result
from pmic_class import pmic
bd71837 = pmic(bd71837)

def test_sanitycheck(command):
    result = bd71837.validate_config('bd71837')
    check_result(result)

    for regulator in bd71837.board.data['regulators'].keys():
        result = bd71837.sanity_check(regulator,command)
        check_result(result)

        result = bd71837.sanity_check_sysfs_en(regulator, command)
        check_result(result)

        result = bd71837.sanity_check_sysfs_set(regulator, command)
        check_result(result)

    for key in bd71837.board.data['debug']:
        result = bd71837.disable_vr_fault(key,command)
        check_result(result)
