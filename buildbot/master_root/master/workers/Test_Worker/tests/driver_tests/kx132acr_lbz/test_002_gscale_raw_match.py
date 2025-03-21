import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import kx132acr_lbz
from test_util import check_result
from sensor_class import sensor
kx132acr_lbz = sensor(kx132acr_lbz)

def test_gscale_raw_match(command):
    result = kx132acr_lbz.test_gscale(command, 'z', 'raw_match', g_tolerance=0.05)
    result = kx132acr_lbz.test_gscale(command, 'y', 'raw_match', g_tolerance=0.05, append_results=True)
    result = kx132acr_lbz.test_gscale(command, 'x', 'raw_match', g_tolerance=0.05, append_results=True)

    check_result(result)
