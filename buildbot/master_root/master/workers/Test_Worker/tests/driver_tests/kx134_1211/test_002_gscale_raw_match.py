import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import kx134_1211
from test_util import check_result
from sensor_class import sensor
kx134_1211 = sensor(kx134_1211)

def test_gscale_raw_match(command):
    result = kx134_1211.test_gscale(command, 'z', 'raw_match', g_tolerance=0.05)
    result = kx134_1211.test_gscale(command, 'y', 'raw_match', g_tolerance=0.05, append_results=True)
    result = kx134_1211.test_gscale(command, 'x', 'raw_match', g_tolerance=0.05, append_results=True)

    check_result(result)
