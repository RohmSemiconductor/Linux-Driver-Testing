import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import kx022acr_z
from test_util import check_result
from sensor_class import sensor
kx022acr_z = sensor(kx022acr_z)

def test_gsel(command):
    for value in kx022acr_z.board.data['settings']['gsel']['list_values']:
        result = kx022acr_z.test_gsel(value, command)
        print(result)
    check_result(result)
