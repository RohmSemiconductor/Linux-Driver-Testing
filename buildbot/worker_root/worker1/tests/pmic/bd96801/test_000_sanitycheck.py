import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd96801
from test_util import check_result
from pmic_class import pmic
bd96801 = pmic(bd96801)

def test_sanitycheck(command):
    result = bd96801.validate_config('bd96801')
    check_result(result)

    for regulator in bd96801.board.data['regulators'].keys():
        result = bd96801.sanity_check(regulator,command)
        check_result(result)

        result = bd96801.sanity_check_sysfs_en(regulator, command)
        check_result(result)

        result = bd96801.sanity_check_sysfs_set(regulator, command)
        check_result(result)
