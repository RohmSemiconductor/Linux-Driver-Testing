import pytest
import sys
import os
import fileinput
from importlib import import_module

from pathlib import Path
from datetime import date
sys.path.append(str(Path('./configs').absolute()))
from pmic_conf import pmic
import bd71847_dts
today = date.today()
todaystr = today.strftime("%d-%m-%Y")
target = sys.argv[1]
target_dts = target+"_dts"


#print(type(target_dts))
imported_dts = __import__(target_dts)


target = pmic(imported_dts)
print(target)
#
#print(type(target))
#print(target.board.dts)
#
test_dts = 'default'
template = 'configs/'+target.board.dts['name']+'_gen_template.dts'
##print(template)
target.generate_dts(test_dts, template,'configs/dts/'+target.board.dts['name']+'/generated_dts_'+test_dts+'.dts')
