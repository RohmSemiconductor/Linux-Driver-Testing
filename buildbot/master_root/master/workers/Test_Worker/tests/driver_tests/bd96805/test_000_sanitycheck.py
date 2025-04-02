import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd96805
from test_util import check_result
from pmic_class import pmic
bd96805 = pmic(bd96805)

def test_sanitycheck(command):
    result = bd96805.validate_config('bd96805')
    check_result(result)

    for regulator in bd96805.board.data['regulators'].keys():
        result = bd96805.sanity_check(regulator,command)
        check_result(result)

        result = bd96805.sanity_check_sysfs_en(regulator, command)
        check_result(result)

        result = bd96805.sanity_check_sysfs_set(regulator, command)
        check_result(result)
