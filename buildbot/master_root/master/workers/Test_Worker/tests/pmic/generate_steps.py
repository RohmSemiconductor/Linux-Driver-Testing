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
if test_type == 'pmic':
    pwd = pwd + '/'+product
elif test_type == 'accelerometer':
    pwd = pwd + '/'+product
elif test_type == 'dts':
    dts = sys.argv[3]
    pwd = pwd + '/'+product+'/dts/'+dts

dir_list = os.listdir(pwd)

pop_list=[]
for i in range(len(dir_list)):
    if ((dir_list[i] == "__pycache__") or (dir_list[i] == "dts") or (dir_list[i] == ".pytest_cache") or (dir_list[i] == "test_000_sanitycheck.py") or (".swp" in dir_list[i])):
        pop_list.append(i)

if len(pop_list) > 0:
    for i in range(len(pop_list)):
        dir_list.pop(pop_list[i]-i)

dir_list = sorted(dir_list)
for i in dir_list:
    print(i)
