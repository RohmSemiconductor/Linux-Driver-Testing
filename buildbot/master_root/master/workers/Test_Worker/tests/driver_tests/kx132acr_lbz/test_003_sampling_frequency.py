import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import kx132acr_lbz
from test_util import check_result
from sensor_class import sensor
kx132acr_lbz = sensor(kx132acr_lbz)
import math

def test_sampling_frequency(command):
    ### In case sampling frequency test is the first test for anything.
    ### A dummy read is needed before setting watermark!

    dummy_read = kx132acr_lbz.read_timestamps(command)
    kx132acr_lbz.set_watermark(command, 5)
    dummy_read = kx132acr_lbz.read_timestamps(command)
    ### assert watermark with i2cget

    for frequency in kx132acr_lbz.board.data['settings']['sampling_frequency']['list_values']:
        count = (math.ceil(frequency) * 2)
        result = kx132acr_lbz.test_sampling_frequency_match_timestamp(command, frequency, watermark=5, count=count, tolerance=10)
        check_result(result)
