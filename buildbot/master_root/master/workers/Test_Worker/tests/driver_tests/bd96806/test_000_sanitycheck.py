import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd96806
from test_util import check_result
from pmic_class import pmic
bd96806 = pmic(bd96806)

def test_sanitycheck(command):
    result = bd96806.validate_config('bd96806')
    check_result(result)

    for regulator in bd96806.board.data['regulators'].keys():
        result = bd96806.sanity_check(regulator,command)
        check_result(result)

        result = bd96806.sanity_check_sysfs_en(regulator, command)
        check_result(result)

        result = bd96806.sanity_check_sysfs_set(regulator, command)
        check_result(result)
