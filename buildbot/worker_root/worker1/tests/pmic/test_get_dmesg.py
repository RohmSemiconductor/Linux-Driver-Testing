import sys
import pytest

sys.path.append('..')
from test_util import report_dmesg, check_result, result

def test_get_dmesg(command, product):
    result['type'] = 'generic'
    result['stage'] = 'get_dmesg'
    result['expect'] = 0
    stdout, stderr, returncode = command.run('dmesg')
    result['return'] = returncode
    if result['return'] == 0:
        report_dmesg(product, stdout)
    check_result(result)
