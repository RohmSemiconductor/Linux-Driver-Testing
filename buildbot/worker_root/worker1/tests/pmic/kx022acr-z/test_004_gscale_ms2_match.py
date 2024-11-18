import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import kx022acr_z
from test_util import check_result
from sensor_class import sensor
kx022acr_z = sensor(kx022acr_z)

from time import sleep

def test_gscale_ms2(command):
    result = kx022acr_z.test_gscale(command, 'z', 'ms2_match', tolerance=0.5)
    result = kx022acr_z.test_gscale(command, 'y', 'ms2_match', append_results=True, tolerance=0.5)
    result = kx022acr_z.test_gscale(command, 'x', 'ms2_match', append_results=True, tolerance=0.5)

    print("iio_generic: "+str(result['return']))
    print("from reg: "+str(result['expect_perfect']))
    print("low_limit: "+str(result['expect_low']))
    print("high_limit: "+str(result['expect_high']))
    print("return_diff: "+str(result['return_diff']))

    check_result(result)
