import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd71815
from test_util import check_result
from pmic_class import pmic
bd71815 = pmic(bd71815)

def test_sanitycheck(command):
    result = bd71815.validate_config('bd71815')
    check_result(result)

    for regulator in bd71815.board.data['regulators'].keys():
        result = bd71815.sanity_check(regulator,command)
        check_result(result)

        if 'dts_only' not in bd71815.board.data['regulators'][regulator].keys(): 
            check_sysfs_en = bd71815.sanity_check_sysfs_en(regulator, command)
            check_result(result)

            check_sysfs_set = bd71815.sanity_check_sysfs_set(regulator, command)
            check_result(result)
