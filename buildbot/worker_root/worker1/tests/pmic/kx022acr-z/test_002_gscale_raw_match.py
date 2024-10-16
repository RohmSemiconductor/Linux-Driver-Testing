import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import kx022acr_z
from test_util import check_result
from sensor_class import sensor
kx022acr_z = sensor(kx022acr_z)

### Only Z-axis is tested in this test. It is the only axis which' value can be relied to be
### fairly close to earths gravitational acceleration.
def test_gscale_raw_match(command):
    result = kx022acr_z.test_gscale(command, 'z', 'raw_match', tolerance=4)
    result = kx022acr_z.test_gscale(command, 'y', 'raw_match', tolerance=3, append_results=True)
    result = kx022acr_z.test_gscale(command, 'x', 'raw_match', tolerance=3, append_results=True)

    check_result(result)
