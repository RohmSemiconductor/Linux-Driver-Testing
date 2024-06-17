import sys
import os
sys.path.append(os.path.abspath("."))

from helpers import *

from time import sleep

def test_init_overlay(command):
    stdout, stderr, returncode = command.run('insmod /mva_overlay.ko')
    if (returncode != 0):
        print(stdout[-1])
#    assert returncode == 0
    #assert stdout
    #assert not stderr
    lsmod,stderr, returncode = command.run('lsmod')
    assert checkStdOut(lsmod,'mva_overlay') == 0
