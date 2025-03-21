import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import kx132acr_lbz
from test_util import check_result
from sensor_class import sensor
kx132acr_lbz = sensor(kx132acr_lbz)

def test_gsel(command):
    for value in kx132acr_lbz.board.data['settings']['gsel']['list_values']:
        result = kx132acr_lbz.test_gsel(value, command)
    check_result(result)
