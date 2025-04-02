import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd96802
from test_util import check_result
from pmic_class import pmic
bd96802 = pmic(bd96802)

def test_sanitycheck(command):
    result = bd96802.validate_config('bd96802')
    check_result(result)

    for regulator in bd96802.board.data['regulators'].keys():
        result = bd96802.sanity_check(regulator,command)
        check_result(result)

        result = bd96802.sanity_check_sysfs_en(regulator, command)
        check_result(result)

        result = bd96802.sanity_check_sysfs_set(regulator, command)
        check_result(result)
