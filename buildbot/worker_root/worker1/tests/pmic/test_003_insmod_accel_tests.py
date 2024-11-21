import pytest
import sys
import copy
sys.path.append('..')
sys.path.append('./configs')
from test_util import checkStdOut, check_result, result
from kernel_modules import *

def test_insmod_tests(command,product):
    result['type'] = 'generic'
    result['stage'] = 'insmod_tests'

    stdout, stderr, returncode = command.run('uname -r')
    lib_mod_dir = copy.copy(stdout[0])


    for x in range(0,len(kernel_modules['test'][product])):
        stdout, stderr, returncode = command.run('cp /'+lib_mod_dir+'/kernel/')
    stdout, stderr, returncode = command.run('depmod')


    for x in range(0,len(kernel_modules['test'][product])):
        mod_name = kernel_modules['test'][product][x].split('.',2)
        stdout, stderr, returncode = command.run('modprobe '+mod_name[0])

    if (returncode != 0):
        print(stdout[-1])
    lsmod, stderr, returncode = command.run('lsmod')

    for x in range(len(kernel_modules['insmod_tests'][product])):
        result['expect'].append([kernel_modules['insmod_tests'][product][x], 0])
        result['return'].append([kernel_modules['insmod_tests'][product][x], checkStdOut(lsmod,kernel_modules['insmod_tests'][product][x])])

    result['lsmod'] = lsmod
    check_result(result)

