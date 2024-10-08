import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import kx022acr_z
from test_util import check_result
from sensor_class import sensor
kx022acr_z = sensor(kx022acr_z)

def test_sampling_frequency(command):

    for frequency in kx022acr_z.board.data['settings']['sampling_frequency']['list_values']:
        result = kx022acr_z.test_sampling_frequency_match_timestamp(frequency, command, tolerance=0.02)
        result['sampling_rate'] = frequency

        check_result(result)
