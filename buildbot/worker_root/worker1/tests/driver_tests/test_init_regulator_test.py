import pytest
import sys
import os
sys.path.append(os.path.abspath("."))

from helpers import *
from kernel_modules import *

def test_init_overlay(command,product): 
    stdout, stderr, returncode = command.run('/./init_regulator_test.sh '+product)
    if (returncode != 0):
        print(stdout[-1])
    assert returncode == 0
        
