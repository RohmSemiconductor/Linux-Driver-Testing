import pytest
import sys
import copy
sys.path.append('..')
sys.path.append('./configs')
from test_util import checkStdOut, check_result, result
from kernel_modules import *

def test_insmod_tests(command,product, result_dir):
    result['type'] = 'generic'
    result['stage'] = 'iio_generic_buffer'
    result['result_dir'] = result_dir
    result['expect'] = '0'

    stdout, stderr, returncode = command.run('ls /iio_generic_buffer; echo $?')

    result['reason'] = stdout[0]
    result['return'] = stdout[1]

    if result['return'] != result['expect']:
        print("iio_generic_buffer binary is not found in the NFS!!\n"+
              "Reason: "+result['reason']+"\n"+
              "Build again from source found @ Linux-Driver-Testing/tools/\n")

    check_result(result)

