import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd9576
from test_util import check_result
from pmic_class import pmic
bd9576 = pmic(bd9576)

def test_sanitycheck(command):
    result = bd9576.validate_config('bd9576')
    check_result(result)

    for regulator in bd9576.board.data['regulators'].keys():
        result = bd9576.sanity_check(regulator,command)
        check_result(result)

        result = bd9576.sanity_check_sysfs_en(regulator, command)
        check_result(result)

        result = bd9576.sanity_check_sysfs_set(regulator, command)
        check_result(result)
