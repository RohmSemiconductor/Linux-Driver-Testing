import pytest
import sys
import os
sys.path.append(os.path.abspath("."))

from helpers import *
from time import sleep
from kernel_modules import *

def test_init_overlay(command,product):
    for x in range(0,len(kernel_modules['dt_overlays'][product])):
        stdout, stderr, returncode = command.run('dd if=/'+kernel_modules['dt_overlays'][product][x]+' of=/sys/kernel/mva_overlay/overlay_add bs=1M')
    if (returncode != 0):
        print(stdout[-1])

    # Sleep is needed because kernel functions take a bit of time
    # to actually load the modules after dd command completes.
    # sleep(2) is enough for now, increase if this test fails
    # for this reason. To manually check false negative, run
    # command lsmod after running the dd command to see if the
    # modules are loaded.
    sleep(2)
    lsmod, stderr, returncode = command.run('lsmod')
    for x in range(len(kernel_modules['merged_dt_overlay'][product])):
        assert checkStdOut(lsmod,kernel_modules['merged_dt_overlay'][product][x]) == 0
