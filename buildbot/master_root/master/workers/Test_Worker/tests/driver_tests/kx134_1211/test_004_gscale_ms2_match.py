import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import kx134_1211
from test_util import check_result
from sensor_class import sensor
kx134_1211 = sensor(kx134_1211)

from time import sleep

def test_gscale_ms2(command):
    result = kx134_1211.test_gscale(command, 'z', 'ms2_match', tolerance=1)
    result = kx134_1211.test_gscale(command, 'y', 'ms2_match', append_results=True, tolerance=1)
    result = kx134_1211.test_gscale(command, 'x', 'ms2_match', append_results=True, tolerance=1)

    print("iio_generic: "+str(result['return']))
    print("from reg: "+str(result['expect_perfect']))
    print("low_limit: "+str(result['expect_low']))
    print("high_limit: "+str(result['expect_high']))
    print("return_diff: "+str(result['return_diff']))

    check_result(result)
