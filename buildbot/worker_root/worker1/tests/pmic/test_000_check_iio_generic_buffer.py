import pytest
import sys
import copy
sys.path.append('..')
sys.path.append('./configs')
from test_util import checkStdOut, check_result, result
from kernel_modules import *

def test_insmod_tests(command,product):
    result['type'] = 'generic'
    result['stage'] = 'iio_generic_buffer'
    result['expect'] = '0'

    stdout, stderr, returncode = command.run('ls /joo/iio_generic_buffer; echo $?')

    result['reason'] = stdout[0]
    result['return'] = stdout[1]

    check_result(result)

