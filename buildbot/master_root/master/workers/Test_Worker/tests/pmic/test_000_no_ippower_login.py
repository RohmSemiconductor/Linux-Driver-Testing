import subprocess
import sys
from pathlib import Path

sys.path.append('..')
from test_util import checkStr, check_result, result
result = result
def test_login(power_port, beagle, result_dir):

    result['type'] = 'generic'
    result['result_dir'] = result_dir
#    result['stage'] = 'ip_power'

#    ip_power = subprocess.run('/bin/bash .././ip-power-control.sh '+power_port+' 0' ,shell=True, capture_output=True, text=True)
#    ip_power = subprocess.run('/bin/bash .././ip-power-control.sh '+power_port+' 1' ,shell=True, capture_output=True, text=True)
#    stdout=''
#    stdout = ip_power.stdout.strip()
#
#    result['expect'] = 0
#    result['return'] = checkStr(stdout,'SetPowerByIdx')
#    check_result(result)

    result['stage'] = 'login'
    test_shell = subprocess.run('pytest --lg-log /tmp/rohm_linux_driver_tests/temp_results/ --lg-env '+beagle+'.yaml _test_000_shell.py',shell=True)
    if test_shell.returncode != 0:
        i = 0
        while test_shell.returncode != 0 and i<5 :
            i=i+1
#            ip_power = subprocess.run('/bin/bash .././ip-power-control.sh '+power_port+' 0' ,shell=True, capture_output=True, text=True)
#            ip_power = subprocess.run('/bin/bash .././ip-power-control.sh '+power_port+' 1' ,shell=True, capture_output=True, text=True)
            test_shell = subprocess.run('pytest --lg-log /tmp/rohm_linux_driver_tests/temp_results/ --lg-env '+beagle+'.yaml _test_000_shell.py',shell=True)

    result['expect'] = [power_port, beagle, 0]
    result['return'] = [power_port, beagle, test_shell.returncode]
    check_result(result)
