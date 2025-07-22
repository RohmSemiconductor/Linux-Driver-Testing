import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd79703
from test_util import check_result
from addac_class import addac
bd79703 = addac(bd79703)

def test_write_read(command):
    sysfs_retval = bd79703.get_sysfs_information(command)
    maxval = bd79703.bits_maxval()
    for channel in bd79703.board.data['info']['channels'].keys():
        for x in range(0, maxval+1):
            result = bd79703.write_and_read_value(command, channel, x, tolerance=150)
            check_result(result)
        set_output_zero = bd79703.write_and_read_value(command, channel, 0)
