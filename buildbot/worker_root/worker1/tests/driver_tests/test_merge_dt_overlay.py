import pytest
import sys
import os
sys.path.append(os.path.abspath("."))

from helpers import *
from time import sleep
from kernel_modules import *

def test_init_overlay(command,product):
   # product = product
    command.run('echo temppwd | sudo -S su')
    sleep(1)
    print(product)
    print(kernel_modules['test'][product][1])
    
    stdout, stderr, returncode = command.run('sudo dd if=/'+kernel_modules['test'][product][0]+' of=/sys/kernel/mva_overlay/overlay_add bs=1M')
    if (returncode != 0):
        print(stdout[-1])
#    assert returncode == 0
#    assert stdout
#    assert not stderr
    assert checkStdOut(stdout,'PM: Cannot get wkup_m3_ipc handle')==0
        
#    assert 'create_sysfs_for_overlays: sysfs created' in stdout[-1]

    stdout, stderr, returncode = command.run('false')
    assert returncode != 0
#    assert not stdout
    assert not stderr
