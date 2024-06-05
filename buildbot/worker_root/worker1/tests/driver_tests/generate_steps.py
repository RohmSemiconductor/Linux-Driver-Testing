import pytest
import subprocess
import sys
import os
from pathlib import Path
#sys.path.append(os.path.abspath("."))
sys.path.append(str(Path('./configs').absolute()))
product = sys.argv[1]
test_type = sys.argv[2]

pwd = os.getcwd()
if test_type == 'regulator':
    pwd = pwd + '/'+product
elif test_type == 'dts':
    pwd = pwd + '/'+product+'/dts'

dir_list = os.listdir(pwd)
x=0
for i in dir_list:
    if "__pycache__" == i:
        dir_list.pop(x)
        x=x+1
dir_list = sorted(dir_list)
for i in dir_list:
    print(i)
