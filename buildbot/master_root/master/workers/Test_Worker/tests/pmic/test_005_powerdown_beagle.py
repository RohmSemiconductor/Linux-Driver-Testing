import subprocess
import sys
from pathlib import Path

sys.path.append('..')
from test_util import checkStr, check_result, result
result = result
def test_005_powerdown_beagle(power_port, beagle):

#    result['type'] = 'generic'
#    result['stage'] = 'ip_power'

    ip_power = subprocess.run('/bin/bash .././ip-power-control.sh '+power_port+' 0' ,shell=True, capture_output=True, text=True)
    stdout=''
    stdout = ip_power.stdout.strip()

#    result['expect'] = 0
#    result['return'] = checkStr(stdout,'SetPowerByIdx')
#    check_result(result)
#
#    result['expect'] = [power_port, beagle, 0]
#    result['return'] = [power_port, beagle, test_shell.returncode]
#    check_result(result)
