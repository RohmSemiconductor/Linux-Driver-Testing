import pytest
import sys
import os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("./configs"))

from helpers import *
from time import sleep
from kernel_modules import *

def test_init_overlay(command,product):

    ####### IF TEST TIMEOUTS, INCREASE TIMEOUT #######
    # This is not well documented in labgrid, but you can pass timeout=##
    # This sets the timeout in seconds, defaults to 30 if not set

    stdout, stderr, returncode = command.run('cd /; ./test_'+product+'.sh',timeout=300)
    if (returncode != 0): 
        print("---- dmesg ----")
        dmesg = command.run('dmesg')
        print(dmesg)
        print("---- end of dmesg ----")
        print(stdout[-1])
        print(stdout)
#    assert returncode == 0
    assert checkStdOut(stdout,'TESTS PASSED')==0
    assert checkStdOut(stdout,'HELPPO HOMMA')==0
