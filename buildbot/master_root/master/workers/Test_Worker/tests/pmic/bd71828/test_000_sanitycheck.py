import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd71828
from test_util import check_result
from pmic_class import pmic
bd71828 = pmic(bd71828)

def test_sanitycheck(command):
    result = bd71828.validate_config('bd71828')
    check_result(result)

    for regulator in bd71828.board.data['regulators'].keys():
        result = bd71828.sanity_check(regulator,command)
        check_result(result)

        result = bd71828.sanity_check_sysfs_en(regulator, command)
        check_result(result)

        result = bd71828.sanity_check_sysfs_set(regulator, command)
        check_result(result)
