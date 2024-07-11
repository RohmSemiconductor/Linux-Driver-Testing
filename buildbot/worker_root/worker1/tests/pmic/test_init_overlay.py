import sys
from pathlib import Path

sys.path.append('..')
from test_util import *

def test_init_overlay(command):
    stdout, stderr, returncode = command.run('insmod /mva_overlay.ko')
    if (returncode != 0):
        print(stdout[-1])
    lsmod,stderr, returncode = command.run('lsmod')

    if checkStdOut(lsmod, 'mva_overlay') != 0:
        generic_step_fail(tf="init_overlay")

    assert checkStdOut(lsmod,'mva_overlay') == 0
