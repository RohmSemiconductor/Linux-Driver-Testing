import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import kx022acr_z
from test_util import check_result
from sensor_class import sensor
kx022acr_z = sensor(kx022acr_z)
import math

def test_sampling_frequency(command):
    ### In case sampling frequency test is the first test for anything.
    ### A dummy read is needed before setting watermark!

    dummy_read = kx022acr_z.read_timestamps(command)
    kx022acr_z.set_watermark(command, 5)
    dummy_read = kx022acr_z.read_timestamps(command)

    for frequency in kx022acr_z.board.data['settings']['sampling_frequency']['list_values']:
        count = (math.ceil(frequency) * 2)
        result = kx022acr_z.test_sampling_frequency_match_timestamp(command, frequency, watermark=5, count=count, tolerance=7)

        check_result(result)
