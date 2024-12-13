import pytest
import sys
import os
import subprocess
import fileinput
from importlib import import_module

from pathlib import Path
from datetime import date
sys.path.append(str(Path('./configs').absolute()))
from pmic_class import pmic

product = sys.argv[1]
test_dts = sys.argv[2]

imported_dts = __import__(product)
product = pmic(imported_dts)

template = 'configs/dts_templates/'+product.board.data['name']+'_gen_template.dts'

stdout = subprocess.run('mkdir -p /tmp/rohm_linux_driver_tests/dts_generated/'+product.board.data['name'], shell=True)

product.generate_dts(test_dts, template,
        '/tmp/rohm_linux_driver_tests/dts_generated/'+product.board.data['name']+'/generated_dts_'+test_dts+'.dts')
