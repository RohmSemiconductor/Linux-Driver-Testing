import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import kx134_1211
from test_util import check_result
from sensor_class import sensor
kx134_1211 = sensor(kx134_1211)
import math

def test_sampling_frequency(command):
    ### In case sampling frequency test is the first test for anything.
    ### A dummy read is needed before setting watermark!

    dummy_read = kx134_1211.read_timestamps(command)
    kx134_1211.set_watermark(command, 5)
    dummy_read = kx134_1211.read_timestamps(command)

    for frequency in kx134_1211.board.data['settings']['sampling_frequency']['list_values']:
        count = (math.ceil(frequency) * 2)
        result = kx134_1211.test_sampling_frequency_match_timestamp(command, frequency, watermark=5, count=count, tolerance=7)

        check_result(result)
