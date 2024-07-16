import subprocess
import sys
from pathlib import Path

sys.path.append('..')
from test_util import *

def test_login(power_port, beagle, type, product):
    initialize_product(type, product)
    result = subprocess.run('/bin/bash .././ip-power-control.sh '+power_port+' 0' ,shell=True, capture_output=True, text=True)
    result = subprocess.run('/bin/bash .././ip-power-control.sh '+power_port+' 1' ,shell=True, capture_output=True, text=True)
    stdout=''
    stdout = result.stdout.strip()
    assert checkStr(stdout,'SetPowerByIdx')==0
    
    test_shell = subprocess.run('pytest --lg-env '+beagle+'.yaml test_shell.py',shell=True)
    if test_shell.returncode != 0:
        i = 0
        while test_shell.returncode != 0 and i<5 :
            i=i+1
            result = subprocess.run('/bin/bash .././ip-power-control.sh '+power_port+' 0' ,shell=True, capture_output=True, text=True)
            result = subprocess.run('/bin/bash .././ip-power-control.sh '+power_port+' 1' ,shell=True, capture_output=True, text=True)
            test_shell = subprocess.run('pytest --lg-env '+beagle+'.yaml test_shell.py',shell=True)

    if test_shell.returncode != 0:
        generic_step_fail(tf='login',power_port=power_port, beagle=beagle)
    assert test_shell.returncode == 0
