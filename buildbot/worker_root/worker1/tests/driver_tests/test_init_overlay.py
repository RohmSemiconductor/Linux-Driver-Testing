import sys
import os
sys.path.append(os.path.abspath("."))

from helpers import *

from time import sleep

def test_init_overlay(command):
    command.run('echo temppwd | sudo -S su')
    sleep(1)
    stdout, stderr, returncode = command.run('sudo insmod /mva_overlay.ko')
    if (returncode != 0):
        print(stdout[-1])
    assert returncode == 0
    assert stdout
    assert not stderr
    assert checkStdOut(stdout,'create_sysfs_for_overlays: sysfs created')==0
        
#    assert 'create_sysfs_for_overlays: sysfs created' in stdout[-1]

    stdout, stderr, returncode = command.run('false')
    assert returncode != 0
    assert not stdout
    assert not stderr
