import pytest
import sys
import os
sys.path.append(os.path.abspath("./configs"))
sys.path.append(os.path.abspath("."))

from helpers import *
from kernel_modules import *

def test_insmod_tests(command,product):
    for x in range(0,len(kernel_modules['test'][product])):
        stdout, stderr, returncode = command.run('insmod /'+kernel_modules['test'][product][x])
    if (returncode != 0):
        print(stdout[-1])
    lsmod, stderr, returncode = command.run('lsmod')
    for x in range(len(kernel_modules['insmod_tests'][product])):
        if checkStdOut(lsmod,kernel_modules['insmod_tests'][product][x]) != 0:
#            insmod_fail(tf, product, kernel_modules['insmod_tests'][product][x])
            print(sys.argv[0])
            generic_step_fail('insmod', product=product, insmod=kernel_modules['insmod_tests'][product][x])
        assert checkStdOut(lsmod,kernel_modules['insmod_tests'][product][x]) == 0

