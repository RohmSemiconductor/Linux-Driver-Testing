import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import kx134_1211
from test_util import check_result
from sensor_class import sensor
kx134_1211 = sensor(kx134_1211)

def test_gsel(command):
    for value in kx134_1211.board.data['settings']['gsel']['list_values']:
        result = kx134_1211.test_gsel(value, command)
        check_result(result)
