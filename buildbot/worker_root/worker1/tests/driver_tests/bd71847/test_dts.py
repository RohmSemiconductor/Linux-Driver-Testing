import pytest
import sys
import os
import fileinput
from pathlib import Path
sys.path.append(str(Path('./configs').absolute()))
import bd71847
from pmic_conf import pmic
bd71847 = pmic(bd71847)
print(sys.path)



def test_dts():
    new_dts= open('new_dts.dts','w+', encoding="utf-8")
    with fileinput.input(files=('configs/bd71847_test_gen_template.dts'), encoding="utf-8") as f:
        
        for line in f:
                print(line,end='',file=new_dts)
                if 'regulator-name = "buck1"' in line:
                
                    print("TESTING;",file=new_dts)
    new_dts.close()
    # for regulator in bd71847.board.data['regulators'].keys():
     #   print(regulator)
    test_fail = 0
    assert test_fail == 1
