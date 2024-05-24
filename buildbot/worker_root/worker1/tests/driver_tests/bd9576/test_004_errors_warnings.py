import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd9576
from pmic_conf import pmic
bd9576 = pmic(bd9576)
print(sys.path)

def test_errors_warnings(command):
#    test = '00000001'
#    test2= '0x00000001'
#    joo = int(test2,0)
#    print(joo)
    for regulator in bd9576.board.data['regulators'].keys():
        print(regulator)
        for setting in bd9576.board.data['regulators'][regulator]['limit_settings']:
            print(setting)
            bd9576.read_dt(regulator,command,setting)
            limit =bd9576.regulator_limit_get(regulator,setting, command)
            print(limit)
             
    test_fail = 0
    assert test_fail == 1
