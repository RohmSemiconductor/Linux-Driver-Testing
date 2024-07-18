import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
from test_util import checkStdOut, check_result, result
from kernel_modules import *

def test_insmod_tests(command,product):
    result['type'] = 'generic'
    result['stage'] = 'insmod_tests'
    for x in range(0,len(kernel_modules['test'][product])):
        stdout, stderr, returncode = command.run('insmod /'+kernel_modules['test'][product][x])
    if (returncode != 0):
        print(stdout[-1])
    lsmod, stderr, returncode = command.run('lsmod')
    for x in range(len(kernel_modules['insmod_tests'][product])):
        result['expect'].append([kernel_modules['insmod_tests'][product][x], 0])
        result['return'].append([kernel_modules['insmod_tests'][product][x], checkStdOut(lsmod,kernel_modules['insmod_tests'][product][x])])

    result['lsmod'] = lsmod
    check_result(result)

