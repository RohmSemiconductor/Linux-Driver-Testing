import sys
from pathlib import Path

sys.path.append('..')
from test_util import checkStdOut, check_result, result

def test_init_overlay(command, result_dir):
    result['type'] = 'generic'
    result['stage'] = 'init_overlay'
    result['result_dir'] = result_dir

    stdout, stderr, returncode = command.run('insmod /mva_overlay.ko')
    if (returncode != 0):
        print(stdout[-1])
    lsmod,stderr, returncode = command.run('lsmod')

    result['lsmod'] = lsmod
    result['expect'] = 0
    result['return'] = checkStdOut(lsmod, 'mva_overlay')
    check_result(result)
