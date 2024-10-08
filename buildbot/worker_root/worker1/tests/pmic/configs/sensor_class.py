from dataclasses import dataclass, field
import pytest
from time import sleep
import sys
import os
import copy
import math
import numbers

from test_class_helpers import bitshift_index_by_bitmask, escape_path
sys.path.append(os.path.abspath("."))

@dataclass
class sensor:
    board: dict
    result: dict = field(default_factory=lambda: {
    'type':         'Sensor',
    'stage':        None,
    'product':      None,
    'return':       [],
    'expect':       [],
    })

    def frequency_to_ns(self, frequency):
        ns = (1/frequency) * pow(10,9)
        return ns

    def find_iio_device_files(self, command):
        stdout, stderr, returncode = command.run("grep -RIn "+self.board.data['iio_device']['name']+" /sys/bus/iio/devices/*/name | sed 's![^/]*$!!'")
        x = 0
        for line in stdout:
            if "iio:" in line:
                correct_path_line = x
            x = x+1

        path = stdout[correct_path_line]
        path = escape_path(path)

        return path

                                                            ### tolerance 0.015 = +/- 1,5%
    def test_sampling_frequency_match_timestamp(self, frequency, command, tolerance=0.015):
        self.result['stage'] = 'test_sampling_frequency_match_timestamp'
        self.result['expect'] = 'range'
        self.result['tolerance'] = tolerance*100

        self.set_sampling_frequency_driver(frequency, command)
        timestamps = self.read_timestamps(command, count = 2)

        frequency_ns = self.frequency_to_ns(frequency)
        self.result['expect_perfect'] = frequency_ns
        timestamp_interval = (int(timestamps[1]) - int(timestamps[0]))
        high_limit =(frequency_ns * tolerance) + frequency_ns
        self.result['expect_high']= high_limit

        low_limit = ((frequency_ns * tolerance) * -1) + frequency_ns
        self.result['expect_low'] = low_limit
        self.result['return'] = timestamp_interval

        self.result['return_diff'] = timestamp_interval - frequency_ns

        return self.result

    def set_sampling_frequency_driver(self, frequency, command):
        frequency = str(frequency)
        path = self.find_iio_device_files(command)
        stdout, stderr, returncode = command.run("echo "+frequency+" > "+path+"/in_accel_sampling_frequency")

    def enable_all_accel_channels(self, command):
        path = self.find_iio_device_files(command)
        stdout, stderr, returncode = command.run("echo 1 > "+path+"/scan_elements/in_accel_x_en")
        stdout, stderr, returncode = command.run("echo 1 > "+path+"/scan_elements/in_accel_y_en")
        stdout, stderr, returncode = command.run("echo 1 > "+path+"/scan_elements/in_accel_z_en")
        stdout, stderr, returncode = command.run("echo 1 > "+path+"/scan_elements/in_timestamp_en")

    def read_timestamps(self, command, count=1):
        self.enable_all_accel_channels(command)
        count_str = str(count)
        stdout = self.read_enabled_channels(command, count=count_str)
        timestamps = self.extract_timestamp_iio_generic_buffer(stdout)

        return timestamps

    def extract_timestamp_iio_generic_buffer(self, stdout):
        split_lines = []
        timestamps = []
        for x in range(0, len(stdout)):
            split_lines.append(stdout[x].split())
        for x in range(0, len(split_lines)):
            timestamps.append(split_lines[x][-1])

        return timestamps

    def read_enabled_channels(self, command, count=1):
        count = str(count)
        stdout, stderr, returncode = command.run("/./iio_generic_buffer -c "+count+" -g -n "+self.board.data['iio_device']['name'])
        return stdout
    def test_gsel(self, scale, command):
        self.result['stage'] = 'test_gsel'
        self.result['expect'] = scale
        self.result['product'] = self.board.data['name']

        self.write_in_accel_scale(scale, command)
        gsel_index = self._i2c_to_gsel_index(command)
        self.result['return'] = self.board.data['settings']['gsel']['list_values'][gsel_index]

        return self.result

    def write_in_accel_scale(self, scale, command):
        scale = str(scale)
        path = self.find_iio_device_files(command)
        stdout, stderr, returncode = command.run("echo "+scale+" > "+path+"in_accel_scale")

        return returncode

    def _i2c_to_gsel_index(self, command):
        stdout, stderr, returncode = command.run("i2cget -f -y "+str(self.board.data['i2c']['bus'])+" "+str(self.board.data['i2c']['address'])+" "+str(self.board.data['settings']['gsel']['reg_address']))

        i2creturn = int(stdout[0],0)
        unmasked_return = i2creturn & self.board.data['settings']['gsel']['reg_bitmask']
        index = bitshift_index_by_bitmask(self.board.data['settings']['gsel']['reg_bitmask'], unmasked_return)

        return index
