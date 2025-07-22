import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd79701
from test_util import check_result
from addac_class import addac
bd79701 = addac(bd79701)

def test_write_read(command):
    sysfs_retval = bd79701.get_sysfs_information(command)
    maxval = bd79701.bits_maxval()
    for channel in bd79701.board.data['info']['channels'].keys():
        for x in range(0, maxval+1):
            result = bd79701.write_and_read_value(command, channel, x, tolerance=130)
            check_result(result)
        set_output_zero = bd79701.write_and_read_value(command, channel, 0)
