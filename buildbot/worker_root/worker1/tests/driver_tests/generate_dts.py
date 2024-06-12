import pytest
import sys
import os
import fileinput
from importlib import import_module

from pathlib import Path
from datetime import date
sys.path.append(str(Path('./configs').absolute()))
from pmic_conf import pmic
today = date.today()
todaystr = today.strftime("%d-%m-%Y")
target = sys.argv[1]
test_dts = sys.argv[2]
target_dts = target

imported_dts = __import__(target_dts)
target = pmic(imported_dts)

template = 'configs/dts_templates/'+target.board.data['name']+'_gen_template.dts'
target.generate_dts(test_dts, template,'configs/dts_generated/'+target.board.data['name']+'/generated_dts_'+test_dts+'.dts')
